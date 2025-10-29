import { useContext, useEffect, useState } from 'react'
import PdfIcon from '../../../../icons/folder.svg'
import Button from '../../../../components/Button'
import { useNavigate } from 'react-router-dom'
import { AppContext } from '../../../../utils/appContext'
import ModalSearchInput from './ModalSearchInput'
import { T, useCurrentLanguage } from '../../../../utils/translations'

export default function ModalSearchWindow() {
  const [result, setResult] = useState<any>(() => [])
  const [toggleSearch, setToggleSearch] = useState(false)
  const [queryCallBack, setQueryCallback] = useState('')
  const [data, setData] = useState<any>(() => [])
  const [dataCategories, setDataCategories] = useState<any[]>([])
  const { setShowSearch } = useContext(AppContext)
  const navigate = useNavigate()
  const lang = useCurrentLanguage()

  useEffect(() => {
    createData(result)
  }, [result])

  const createData = (res: any) => {
    if (res) {
      let data: any[] = []
      res.map((item: any) =>
        item.languages.map((lang: string) => {
          if (item[lang].type === 'document' || item[lang].type === 'design') {
            data.push(item[lang])
          }
        })
      )
      categorizeData(data)
      setData(data)
    }
  }

  const categorizeData = (data: any[]) => {
    let categories: any[] = []
    data.map((item) => {
      if (!categories.includes(item.docclass) && item.docclass !== null) {
        categories.push(item.docclass)
      }
    })
    setDataCategories(categories)
  }

  const showMore = (category: string) => {
    setShowSearch(false)
    navigate('/search/' + queryCallBack + '/' + category)
  }

  const getCategoryFilteredData = (category: string) => {
    var filteredData: any[] = data.filter((x: any) => x.docclass === category)
    return filteredData
  }

  const renderCategories = () => {
    return (
      <div className="flex flex-col lg:flex-row lg:flex-wrap">
        {dataCategories.map((category, i) => {
          return (
            <div
              key={category + ' ' + i}
              className="flex flex-col lg:w-1/2 2xl:w-1/2 mb-8"
            >
              <div className="lg:w-4/5">
                <div className="font-bold lg:text-md">
                  {T(lang, category.toString().toUpperCase())}
                </div>
                {renderCategorizedData(category)}
              </div>
            </div>
          )
        })}
      </div>
    )
  }

  const renderCategorizedData = (category: string) => {
    var filteredData = getCategoryFilteredData(category)

    return (
      <div className="flex flex-col">
        {filteredData.slice(0, 5).map((value: any, i) => {
          return (
            <div key={value.dbid + ' ' + i}>
              {value.docclass === category && (
                <div className="flex flex-row items-center border-b border-purple border-opacity-25 py-2">
                  <div className="my-2 text-xs md:text-sm w-3/4 leading-4">
                    {value.title && value.title.length > 0
                      ? value.title
                      : value.namingcataloguename}
                  </div>
                  {value.files && value.files.length > 0 && (
                    <Button
                      className="ml-auto px-4 py-1 bg-black-light hover:bg-black"
                      size="xs"
                      href={`/customer/${value.files[0].fileName}`}
                      target="_blank"
                    >
                      <img className="w-5" alt="Pdf icon" src={PdfIcon} />
                    </Button>
                  )}
                </div>
              )}
            </div>
          )
        })}
        <div className="mt-4">
          <Button
            onClick={() => showMore(category)}
            className="bg-gray hover:bg-purple hover:text-white text-black"
            size="sm"
          >
            {T(lang, 'showMore')} ({getCategoryFilteredData(category).length})
          </Button>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-xl mt-2 w-full">
      <div className="flex flex-col">
        <ModalSearchInput
          setResult={setResult}
          result={data}
          setQueryCallback={setQueryCallback}
          showTableButton={true}
          setToggleSearch={setToggleSearch}
          toggleSearch={toggleSearch}
        />

        {data.length > 0 && (
          <div className="flex flex-col items-center justify-center lg:items-start lg:justify-start pb-6">
            <div className="w-full max-h-[60vh] md:max-h-[70vh] bg-white scrollbar-thin lg:scrollbar scrollbar-track-white scrollbar-thumb-purple">
              <div className="px-8">{renderCategories()}</div>
            </div>
          </div>
        )}
        {data.length === 0 && toggleSearch && (
          <div className="flex flex-col items-center justify-center lg:items-start lg:justify-start pb-6">
            <div className="px-4"> {T(lang, 'noData')}</div>
          </div>
        )}
      </div>
    </div>
  )
}
