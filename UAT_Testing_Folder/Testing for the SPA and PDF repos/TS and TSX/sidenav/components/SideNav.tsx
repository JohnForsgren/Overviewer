// @ts-nocheck
// UAT example (SideNav component). Types disabled.
import Structure from './Structure'
import arrowRight from '../../../icons/arrow_double_right.svg'
import arrowLeft from '../../../icons/arrow_double_left.svg'
import logo from '../../../images/logo.svg'
import DccKksSearch from '../../dccKksSearch/components/DccKksSearch'
import { Link } from 'react-router-dom'
import { useContext } from 'react'
import { DataContext } from '../../../utils/dataContext'
import {
  useCurrentLanguage,
  useFallBackLanguage
} from '../../../utils/translations'
import DashboardSearch from '../../dashboard/components/DashboardSearch'

type SideNavProps = {
  collapsed: boolean
  setCollapsed: (value: boolean) => void
}

export default function SideNav({ collapsed, setCollapsed }: SideNavProps) {
  const { manual, systemInfo } = useContext(DataContext)
  const language = useCurrentLanguage()
  const fallBackLanguage = useFallBackLanguage(language)
  const isDDP = systemInfo?.element.elementtype === 'DDP' || 'Manual Collection'

  const SideNavCollapsed = () => (
    <button
      onClick={() => setCollapsed(!collapsed)}
      className="fixed w-20 bg-white h-screen p-2 flex flex-col items-center"
    >
      <img className="h-8 w-8 mt-8" alt="Arrow right" src={arrowRight} />
    </button>
  )

  const SideNavOpen = () => (
    <div className="fixed w-80 2xl:w-96 bg-white h-full px-1 tour-1">
      <div className="flex flex-col">
        <div className="pt-6 px-6 pb-4">
          <div className="flex flex-row mb-4">
            <div className="flex w-full justify-center items-center">
              <Link className="" to="/">
                {' '}
                <img className="h-10" alt="Siemens Energy Logo" src={logo} />
              </Link>
            </div>
            <button
              className="p-2 ml-auto"
              onClick={() => setCollapsed(!collapsed)}
            >
              <img className="h-8 w-8" alt="Arrow left" src={arrowLeft} />
            </button>
          </div>

          <div className="">
            {isDDP && manual && (
              <h3 className="font-semibold text-sm ml-2 my-4">
                {manual[language] ?? manual[fallBackLanguage]}
              </h3>
            )}
          </div>
          <DashboardSearch />
        </div>
        <Structure />
      </div>
    </div>
  )

  return (
    <div className="hidden lg:block">
      {collapsed ? <SideNavCollapsed /> : <SideNavOpen />}
    </div>
  )
}
