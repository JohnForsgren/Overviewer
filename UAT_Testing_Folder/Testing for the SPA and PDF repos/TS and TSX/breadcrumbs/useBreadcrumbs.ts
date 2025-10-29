import { useContext } from 'react'
import { DataContext } from '../../utils/dataContext'
import {
  T,
  useCurrentLanguage,
  useFallBackLanguage
} from '../../utils/translations'
import { Breadcrumb } from './types'

export default function useBreadcrumbs() {
  const { structure, dccTree, kksTree, setBreadcrumbs } =
    useContext(DataContext)

  const language = useCurrentLanguage()
  const fallbackLanguage = useFallBackLanguage(language)

  const createBreadCrumbs = (id: any, route: string) => {
    let breakLoop = false
    let res: Breadcrumb[] = []

    const findBreadcrumbs = (children: any[]) => {
      children.map((item: any) => {
        if (item.dbid == id) {
          let breadcrumb: Breadcrumb = {
            dbid: item.dbid,
            title: item[language] ?? item[fallbackLanguage],
            route: '/' + route + '/' + item.dbid
          }
          res.push(breadcrumb)
          breakLoop = true
          return
        }

        if (breakLoop) return

        //If item is within the parent, add the parent
        if (item.children) {
          findBreadcrumbs(item.children)
          if (res.some((element) => element.dbid == id)) {
            let breadcrumb: Breadcrumb = {
              dbid: item.dbid,
              title: item[language] ?? item[fallbackLanguage],
              route: '/' + route + '/' + item.dbid
            }
            res.push(breadcrumb)
          }
        }
      })
    }

    const createStaticBreadcrumb = (name: string) => {
      let breadcrumb: Breadcrumb = {
        title: name,
        route: '',
        dbid: ''
      }
      res.push(breadcrumb)
      setBreadcrumbs(res)
    }

    switch (route) {
      case 'id':
        findBreadcrumbs(structure)
        setBreadcrumbs(res)
        break
      case 'dcc':
        findBreadcrumbs(dccTree)
        setBreadcrumbs(res)
        break
      case 'kks':
        findBreadcrumbs(kksTree)
        setBreadcrumbs(res)
        break
      case 'home':
        createStaticBreadcrumb('Home')
        break
      case 'faq':
        createStaticBreadcrumb('FAQ')
        break
      case 'search':
        createStaticBreadcrumb(T(language, 'search'))
        break
      case 'documents':
        createStaticBreadcrumb(T(language, 'allDocuments'))
        break
      default:
        findBreadcrumbs(structure)
        setBreadcrumbs(res)
    }
  }

  return [createBreadCrumbs]
}
