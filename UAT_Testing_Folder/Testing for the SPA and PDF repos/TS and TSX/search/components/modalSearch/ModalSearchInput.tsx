import { useContext, useState } from 'react'
import SearchIcon from '../../../../icons/search.svg'
import { QuerySearch } from '../../effects'
import { T, useCurrentLanguage } from '../../../../utils/translations'
import { AppContext } from '../../../../utils/appContext'
import { validateSearchInput } from '../../../../helpers/Search'
import { useNavigate } from 'react-router-dom'
import Button from '../../../../components/Button'

type props = {
  setResult: (value: any) => void
  setQueryCallback?: (value: string) => void
  result?: any[]
  showTableButton?: boolean
  setToggleSearch: (value: any) => void
  toggleSearch: boolean
}

export default function ModalSearchInput({
  setResult,
  setQueryCallback,
  result,
  showTableButton,
  setToggleSearch,
  toggleSearch
}: props) {
  const [searchValue, setSearchValue] = useState('')
  const { setLoading, setShowSearch } = useContext(AppContext)
  const lang = useCurrentLanguage()
  const navigate = useNavigate()

  const handleChange = async (e: any) => {
    setSearchValue(e.target.value)
    if (setQueryCallback) {
      setQueryCallback(e.target.value)
    }

    if (toggleSearch) {
      setToggleSearch(false)
    }
  }

  const handleKeyPress = async (e: any) => {
    if (e.which === 13) {
      await doSearch()
    }
  }

  const doSearch = async () => {
    if (validateSearchInput(searchValue)) {
      setResult(await getSearchResults(searchValue))
      setTimeout(() => {
        setToggleSearch(true)
      }, 300)
    }
  }

  const getSearchResults = async (val: string) => {
    setLoading(true)
    const res = await QuerySearch(val, -1, true)
    setLoading(false)
    if (res.children) {
      return res.children
    } else {
      return []
    }
  }

  const viewAsTable = () => {
    setShowSearch(false)
    navigate('/search/' + searchValue)
  }

  const hasResult = result && result.length > 0

  return (
    <>
      <div
        className={`${
          hasResult ? 'border-b border-black border-opacity-20' : ''
        } flex flex-row`}
      >
        <input
          autoFocus
          onKeyDown={handleKeyPress}
          onChange={(e) => handleChange(e)}
          className={`${
            hasResult ? 'rounded-t-lg' : 'rounded-lg'
          } bg-white rounded-t-lg text-xl outline-none ring-0 w-full p-2 px-4`}
          placeholder={T(lang, 'search')}
          value={searchValue}
        ></input>
        <button
          className={`${
            validateSearchInput(searchValue)
              ? 'bg-purple-bright'
              : 'bg-gray-dark'
          }  ${
            hasResult
              ? 'rounded-tr-lg border-b border-black border-opacity-20'
              : 'rounded-br-lg rounded-tr-lg'
          } flex items-center p-4 `}
          onClick={doSearch}
        >
          <img alt="Search" src={SearchIcon} />
        </button>
      </div>
      {hasResult && showTableButton && (
        <div className="flex flex-col md:flex-row px-4 py-2">
          <div className="flex items-center">
            <Button
              onClick={() => viewAsTable()}
              className="my-2 md:mx-4"
              size="xs"
            >
              {T(lang, 'viewAsTable')}
            </Button>
          </div>
        </div>
      )}
    </>
  )
}
