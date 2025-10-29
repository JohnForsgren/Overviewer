// @ts-nocheck
// Example file for UAT context enrichment demonstration. Not part of the runnable project; TypeScript errors intentionally ignored.
import { TourProvider } from '@reactour/tour'
import React, { useEffect, useState } from 'react'
import { HashRouter, Routes, Route } from 'react-router-dom'
import LoadingScreen from './components/LoadingScreen'
import { Breadcrumb } from './features/breadcrumbs/types'
import ContainerChangeManual from './features/changeManual/components/ContainerChangeManual'
import { getManuals } from './features/changeManual/effects'
import ContainerFileModal from './features/files/components/ContainerFileModal'
import MobileHeader from './features/header/components/MobileHeader'
import ContainerSearchWindow from './features/search/components/modalSearch/ContainerSearchWindow'
import {
  getAllDesigns,
  getAllDocuments,
  getAllParts,
  getInitialStructure,
  getTableOfContents
} from './features/sidenav/effects'
import ContainerSystemInfoModal from './features/systemInfo/components/ContainerSystemModal'
import Dcc from './pages/Dcc'
import Documents from './pages/Documents'
import FAQ from './pages/FAQ'
import Home from './pages/Home'
import Id from './pages/Id'
import Kks from './pages/Kks'
import Search from './pages/Search'
import { AppContext } from './utils/appContext'
import { DataContext } from './utils/dataContext'
function App() {
  const storedManualId = JSON.parse(localStorage.getItem('manualId') as string)
  const [showSearch, setShowSearch] = useState<boolean>(false)
  const [modalFiles, setModalFiles] = useState<any[]>([])
  const [showChangeManual, setShowChangeManual] = useState<boolean>(false)
  const [showSystemInfo, setShowSystemInfo] = useState<boolean>(false)
  const [manual, setManual] = useState()
  const [selectableManuals, setSelectableManuals] = useState<any[]>([])
  const [manualId, setManualId] = useState<string | undefined>()
  const [toc, setToc] = useState('')
  const [loading, setLoading] = useState(false)
  const [structure, setStructure] = useState<any[]>([])
  const [allDocuments, setAllDocuments] = useState<any[]>([])
  const [dccTree, setDccTree] = useState<any>([])
  const [kksTree, setKksTree] = useState<any>([])
  const [breadcrumbs, setBreadcrumbs] = useState<Breadcrumb[]>([])
  const [expandedNavigation, setExpandedNavigation] = useState<number[]>([])
  const [selectableLanguages, setSelectableLanguages] = useState<string[]>([])
  const [language, setLanguage] = useState('en')
  const [systemInfo, setSystemInfo] = useState()
  const validManualTypes: string[] = [
    'Manual',
    'Assembly Manual',
    'I&C Manual',
    'Manufacturing Record Book'
  ]

  useEffect(() => {
    if (manualId === undefined) return
    const getManualData = async () => {
      setLoading(true)

      const res = await getInitialStructure(manualId)
      const allDocumentsRes = await getAllDocuments(manualId)
      const allDesignsRes = await getAllDesigns(manualId)
      const allPartsRes = await getAllParts(manualId)
      const tocRes = await getTableOfContents(manualId)

      setLoading(false)
      setDccTree(res.dccTree.children)
      setKksTree(res.kksTree.children)
      setManual(res.structure)
      setStructure(res.structure.children)

      const docsAndDesigns = allDocumentsRes.children.concat(
        allDesignsRes.children
      )

      const docsDesignsAndParts = docsAndDesigns.concat(allPartsRes.children)

      setAllDocuments(docsDesignsAndParts)
      const tocLang = tocRes.element.languages[0]
      setToc(`/customer/toc_${tocRes.element[tocLang].doc_id}.pdf`)
    }

    getManualData()
    setBreadcrumbs([])
    localStorage.setItem('manualId', JSON.stringify(manualId))
  }, [manualId])

  useEffect(() => {
    const getData = async () => {
      const manualsRes = await getManuals()
      const startupLanguage = manualsRes.languages.includes('en')
        ? 'en'
        : manualsRes.languages[0]
      setSystemInfo(manualsRes)
      createSelectableManuals(manualsRes.children, startupLanguage)
      setSelectableLanguages(manualsRes.languages)
      setLanguage(startupLanguage)

      if (storedManualId) {
        setManualId(storedManualId)
        return
      }

      if (validManualTypes.includes(manualsRes.element.elementtype)) {
        setManualId(manualsRes.element.dbId)

        //If DDP select first manual child
      } else if (!storedManualId && manualsRes.children.length > 1) {
        const dbid =
          manualsRes.children[0][startupLanguage]?.dbid ??
          manualsRes.children[0]['en'].dbid
        setManualId(dbid)
      }
    }

    getData()
    // eslint-disable-next-line
  }, [storedManualId])

  useEffect(() => {
    localStorage.setItem('breadcrumbs', JSON.stringify(breadcrumbs))
  }, [breadcrumbs])

  const createSelectableManuals = (res: any, startupLanguage: string) => {
    let data: any[] = []
    res.map((item: any) => {
      if (
        (item[startupLanguage] &&
          validManualTypes.includes(item[startupLanguage].type)) ||
        (item[language] && validManualTypes.includes(item[language]))
      ) {
        data.push(item)
      }
    })
    setSelectableManuals(data)
  }

  return (
    <TourProvider
      styles={{
        badge: (base) => ({
          ...base,
          backgroundColor: '#641E8C'
        }),
        popover: (base) => ({
          ...base,
          borderRadius: 15,
          paddingTop: 35
        })
      }}
      steps={[]}
    >
      <div className="">
        <AppContext.Provider
          value={{
            showSearch,
            setShowSearch,
            modalFiles,
            setModalFiles,
            showChangeManual,
            setShowChangeManual,
            showSystemInfo,
            setShowSystemInfo,
            language,
            setLanguage,
            selectableLanguages,
            loading,
            setLoading
          }}
        >
          <DataContext.Provider
            value={{
              systemInfo,
              manual,
              setManual,
              manualId,
              setManualId,
              toc,
              selectableManuals,
              structure,
              allDocuments,
              dccTree,
              kksTree,
              breadcrumbs,
              setBreadcrumbs,
              expandedNavigation,
              setExpandedNavigation
            }}
          >
            <HashRouter>
              <LoadingScreen />
              <ContainerChangeManual />
              <ContainerSearchWindow />
              <ContainerSystemInfoModal />
              <ContainerFileModal />
              <MobileHeader />
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="id/:id" element={<Id />} />
                <Route path="dcc/:id" element={<Dcc />} />
                <Route path="kks/:id" element={<Kks />} />
                <Route path="search/:query" element={<Search />} />
                <Route path="search/:query/:category" element={<Search />} />
                <Route path="search" element={<Search />} />
                <Route path="documents" element={<Documents />} />
                <Route path="faq" element={<FAQ />} />
              </Routes>
            </HashRouter>
          </DataContext.Provider>
        </AppContext.Provider>
      </div>
    </TourProvider>
  )
}

export default App
