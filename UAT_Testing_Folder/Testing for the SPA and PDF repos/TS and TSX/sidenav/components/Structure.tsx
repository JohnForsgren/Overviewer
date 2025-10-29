// @ts-nocheck
// UAT example (Structure component). Ignoring type checks.
import { useContext, useLayoutEffect } from 'react'
import { NavLink } from 'react-router-dom'
import { DataContext } from '../../../utils/dataContext'
import {
  T,
  useCurrentLanguage,
  useFallBackLanguage
} from '../../../utils/translations'

export default function Structure() {
  const { structure, expandedNavigation, setExpandedNavigation, toc, manual } =
    useContext(DataContext)
  const language = useCurrentLanguage()
  const fallBackLanguage = useFallBackLanguage(language)

  useLayoutEffect(() => {
    scrollToElement(localStorage.getItem('clickedNav'))
  }, [])

  const toggleMenuItem = (item: any) => {
    const id = item.dbid
    localStorage.setItem('clickedNav', item.dbid)
    if (expandedNavigation.includes(id)) {
      //Close menu item
      setExpandedNavigation((current: number[]) =>
        current.filter((dbid) => dbid !== id)
      )
      collapseChildren(item.children)
    } else {
      //Add
      setExpandedNavigation((arr: number[]) => [...arr, id])
    }
  }

  //Close all sub menu items
  const collapseChildren = (children: any[]) => {
    if (children) {
      children.forEach((child: any) => {
        setExpandedNavigation((current: number[]) =>
          current.filter((dbid) => dbid !== child.dbid)
        )
        collapseChildren(child.children)
      })
    }
  }

  const expandChildren = (children: any[], addMargin: boolean) => {
    return children.map((item: any) => {
      let isOpen = expandedNavigation.includes(item.dbid)
      return (
        <div
          id={item.dbid}
          className={`${
            addMargin && 'ml-4'
          } flex flex-col text-sm text-black cursor-pointer hover:text-purple`}
          key={item.dbid}
        >
          {item.children ? (
            <>
              <div className="flex flex-row mt-2">
                <button
                  className={`${
                    isOpen
                      ? 'before:content-uparrow'
                      : 'before:content-downarrow'
                  }`}
                  onClick={() => toggleMenuItem(item)}
                ></button>
                <div className={`${isOpen && 'underline '}`}>
                  <NavLink
                    className={({ isActive }) =>
                      isActive ? 'text-black font-semibold' : ''
                    }
                    onClick={() => toggleMenuItem(item)}
                    to={`/id/${item.dbid}`}
                  >
                    {item[language] ?? item[fallBackLanguage]}
                  </NavLink>
                </div>
              </div>

              {isOpen && expandChildren(item.children, isOpen)}
            </>
          ) : (
            <NavLink
              className={({ isActive }) =>
                isActive ? 'text-black font-semibold my-1 ml-6' : 'my-1 ml-6'
              }
              onClick={() => localStorage.setItem('clickedNav', item.dbid)}
              to={`/id/${item.dbid}`}
            >
              <span className="">
                {item[language] ?? item[fallBackLanguage]}
              </span>
            </NavLink>
          )}
        </div>
      )
    })
  }

  const expandChildrenM3Project = (children: any[], addMargin: boolean) => {
    return children.map((item: any) => {
      let containsHG = item[language].includes('HG')
      let isOpen = expandedNavigation.includes(item.dbid)
      return (
        <div
          id={item.dbid}
          className={`${
            addMargin && 'ml-4'
          } flex flex-col text-sm text-black cursor-pointer hover:text-purple`}
          key={item.dbid}
        >
          {item.children ? (
            <>
              <div className="flex flex-row mt-2">
                {!containsHG && (
                  <button
                    className={`${
                      isOpen
                        ? 'before:content-uparrow'
                        : 'before:content-downarrow'
                    }`}
                    onClick={() => toggleMenuItem(item)}
                  ></button>
                )}
                <div className={`${isOpen && !containsHG && 'underline '}`}>
                  <NavLink
                    className={({ isActive }) =>
                      `${isActive ? 'text-black font-semibold' : ''} ${
                        containsHG ? 'my-1 ml-6' : ''
                      }`
                    }
                    onClick={() => toggleMenuItem(item)}
                    to={`/id/${item.dbid}`}
                  >
                    {item[language] ?? item[fallBackLanguage]}
                  </NavLink>
                </div>
              </div>

              {isOpen &&
                !containsHG &&
                expandChildrenM3Project(item.children, isOpen)}
            </>
          ) : (
            <NavLink
              className={({ isActive }) =>
                isActive ? 'text-black font-semibold my-1 ml-6' : 'my-1 ml-6'
              }
              onClick={() => localStorage.setItem('clickedNav', item.dbid)}
              to={`/id/${item.dbid}`}
            >
              <span className="">
                {item[language] ?? item[fallBackLanguage]}
              </span>
            </NavLink>
          )}
        </div>
      )
    })
  }

  function scrollToElement(dbid: any) {
    var topPos = document.getElementById(`${dbid}`)?.offsetTop
    var scroll = document.getElementById('scroll')

    if (scroll && topPos) {
      scroll.scrollTop = topPos - 300
    }
  }

  return (
    <div className="pb-6 mt-4 lg:mt-0">
      <div
        id="scroll"
        className="lg:max-h-[70vh] scrollbar-thin scrollbar-track-white scrollbar-thumb-purple track-scroll"
      >
        <div className="lg:px-4 lg:pb-8">
          {structure && structure.length > 0 ? (
            manual[language].includes('M3') ||
            manual[language].includes('Site Assembly') ? (
              <div>{expandChildrenM3Project(structure, false)}</div>
            ) : (
              <div>{expandChildren(structure, false)}</div>
            )
          ) : null}
          <div className="h-0.5 w-full border-b-2 border-gray-dark border-opacity-50 my-2"></div>
          <div
            id="documents"
            className="flex flex-col text-sm text-black italic cursor-pointer hover:text-purple ml-6 my-1"
          >
            <NavLink
              className={({ isActive }) => (isActive ? 'text-purple' : '')}
              onClick={() => localStorage.setItem('clickedNav', 'documents')}
              to="/documents"
            >
              {T(language, 'allDocuments')}
            </NavLink>
          </div>
          <div
            id="documents"
            className="flex flex-col text-sm text-black italic cursor-pointer hover:text-purple ml-6 my-1"
          >
            <a href={toc} target="_blank" rel="noreferrer">
              {T(language, 'tableOfContents')}
            </a>
          </div>
        </div>
      </div>
    </div>
  )
}
