import { useContext, useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { DataContext } from '../../../utils/dataContext'
import { Breadcrumb } from '../types'

type props = {
  className?: string
}
export default function Breadcrumbs({ className }: props) {
  const { breadcrumbs } = useContext(DataContext)
  const { setExpandedNavigation, expandedNavigation } = useContext(DataContext)

  const [createdBreadcrumbs, setCreatedBreadcrumbs] = useState<Breadcrumb[]>([])

  const createBreadcrumbs = () => {
    let res: Breadcrumb[] = []
    breadcrumbs
      .slice(0)
      .reverse()
      .map((item) => res.push(item))
    setCreatedBreadcrumbs(res)
  }

  useEffect(() => {
    createBreadcrumbs()
  }, [breadcrumbs])

  const handleClick = (dbid: any) => {
    localStorage.setItem('clickedNav', dbid)
    if (!expandedNavigation.includes(dbid)) {
      setExpandedNavigation((arr: number[]) => [...arr, dbid])
    }
  }

  return (
    <div
      className={`${className} flex flex-row flex-wrap text-white text-xs lg:text-md mt-0`}
    >
      {createdBreadcrumbs.map((breadcrumb, index) => (
        <div key={index}>
          <Link
            onClick={() => handleClick(breadcrumb.dbid)}
            className="hover:text-gray-dark"
            to={`${breadcrumb.route}`}
          >
            {' '}
            {breadcrumb.title ? breadcrumb.title : breadcrumb.dbid}
          </Link>

          <span className="mx-1">/</span>
        </div>
      ))}
    </div>
  )
}

Breadcrumbs.defaultProps = {
  className: ''
}
