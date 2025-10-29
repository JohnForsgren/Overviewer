import { useContext } from 'react'
import { useNavigate } from 'react-router-dom'
import { AppContext } from '../../../utils/appContext'
import { DataContext } from '../../../utils/dataContext'
import {
  T,
  useCurrentLanguage,
  useFallBackLanguage
} from '../../../utils/translations'
import closeIcon from '../../../icons/close_dark.svg'

export default function ChangeManualModal() {
  const { selectableManuals, setManualId } = useContext(DataContext)
  const { setShowChangeManual } = useContext(AppContext)
  const navigate = useNavigate()
  const lang = useCurrentLanguage()
  const fallBackLanguage = useFallBackLanguage(lang)

  const changeManual = (id: string) => {
    setManualId(id)
    setShowChangeManual(false)
    navigate('/')
  }

  return (
    <div className="p-2 bg-white rounded-xl max-h-[80%]">
      <div className="flex items-center justify-between bg-white rounded-t-xl font-semibold text-xl 2xl:text-2xl text-center p-4 border-b border-black border-opacity-20">
        {T(lang, 'selectManual')}
        <button onClick={() => setShowChangeManual(false)} className="">
          <img alt="close" src={closeIcon} />
        </button>
      </div>

      <div className="pr-8 max-h-[80%] scrollbar-thin scrollbar-thumb-purple">
        <div className="flex flex-col justify-start items-start p-6 space-y-6">
          {selectableManuals.map((manual: any, index: number) => (
            <button
              onClick={() =>
                changeManual(
                  manual[lang]
                    ? manual[lang].dbid
                    : manual[fallBackLanguage].dbid
                )
              }
              key={index}
              className="text-start 2xl:text-xl hover:underline"
            >
              {manual[lang]
                ? manual[lang].title
                : manual[fallBackLanguage].title}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}
