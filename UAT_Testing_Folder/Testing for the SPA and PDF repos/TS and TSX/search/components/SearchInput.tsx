import { useContext, useEffect, useState } from 'react'
import SearchIcon from '../../../icons/search.svg'
import { QuerySearch } from '../effects'
import { DataContext } from '../../../utils/dataContext'
import {
  T,
  useCurrentLanguage,
  useFallBackLanguage
} from '../../../utils/translations'
import { AppContext } from '../../../utils/appContext'
import { validateSearchInput } from '../../../helpers/Search'

type props = {
  setResult: (value: any) => void
  query?: string
  category?: string
}

export default function SearchInput({ setResult, query, category }: props) {
  const [searchValue, setSearchValue] = useState('')
  const [allManuals, setAllManuals] = useState(true)
  const [pdfTextSearch, setPdfTextSearch] = useState(true)
  const { manual, selectableManuals } = useContext(DataContext)
  const { setLoading } = useContext(AppContext)
  const lang = useCurrentLanguage()
  const fallBackLanguage = useFallBackLanguage(lang)

  useEffect(() => {
    const instantSearch = async () => {
      if (query !== undefined && query.length > 1) {
        const res = await getSearchResults(query)
        if (category) {
          createCategorizedResult(res)
        } else {
          setResult(res)
        }
        setSearchValue(query)
      }
    }
    if (query) {
      instantSearch()
    }
  }, [query, category])

  const handleChange = async (e: any) => {
    setSearchValue(e.target.value)
  }

  const handleKeyPress = async (e: any) => {
    if (e.which === 13) {
      await doSearch()
    }
  }

  const doSearch = async () => {
    if (validateSearchInput(searchValue)) {
      setResult(await getSearchResults(searchValue))
    }
  }

  const createCategorizedResult = (result: any[]) => {
    let data: any[] = []
    result.map((item: any) => {
      if (
        item[lang]?.docclass?.toLowerCase() === category?.toLowerCase() ||
        item[fallBackLanguage]?.docclass?.toLowerCase() ===
          category?.toLowerCase()
      ) {
        data.push(item)
      }
    })
    setResult(data)
  }

  const getSearchResults = async (val: string) => {
    const all = allManuals ? -1 : manual?.dbid ? manual.dbid : -1
    setLoading(true)
    const res = await QuerySearch(val, all, pdfTextSearch)
    setLoading(false)
    return res.children
  }

  return (
    <>
      <div className="flex flex-row border-b border-black border-opacity-20">
        <input
          onKeyDown={handleKeyPress}
          onChange={(e) => handleChange(e)}
          className="bg-white rounded-t-lg text-xl outline-none ring-0 w-full p-2 px-4"
          placeholder={T(lang, 'search')}
          value={searchValue}
        ></input>
        <button
          className={`${
            validateSearchInput(searchValue)
              ? 'bg-purple-bright'
              : 'bg-gray-dark'
          }  rounded-tr-lg flex items-center p-4 border-b border-black border-opacity-20`}
          onClick={doSearch}
        >
          <img alt="Search" src={SearchIcon} />
        </button>
      </div>
      <div className="flex flex-col md:flex-row px-4 pt-4">
        {selectableManuals.length > 1 && (
          <div className="flex flex-row items-center">
            <label>{T(lang, 'allManuals')}</label>
            <input
              checked={allManuals}
              onChange={() => setAllManuals(!allManuals)}
              className="accent-purple-bright mx-2"
              type="checkbox"
            />
          </div>
        )}
        <div className="flex flex-row items-center">
          <label>{T(lang, 'documentContent')}</label>
          <input
            checked={pdfTextSearch}
            onChange={() => setPdfTextSearch(!pdfTextSearch)}
            className="accent-purple-bright mx-2"
            type="checkbox"
          />
        </div>
      </div>
    </>
  )
}
