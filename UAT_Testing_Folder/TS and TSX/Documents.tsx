// @ts-nocheck
// UAT example (Documents). Non-operational stub.
import { useContext, useEffect } from 'react'
import Page from '../components/Page'
import useBreadcrumbs from '../features/breadcrumbs/useBreadcrumbs'
import Table from '../features/table/components/Table'
import { AppContext } from '../utils/appContext'
import { DataContext } from '../utils/dataContext'

export default function Documents() {
  const [createBreadCrumbs] = useBreadcrumbs()
  const { structure, allDocuments } = useContext(DataContext)
  const { language } = useContext(AppContext)

  useEffect(() => {
    if (structure !== undefined) {
      createBreadCrumbs('', 'documents')
    }
  }, [structure, language])

  return (
    <Page>
      <Table incomingData={allDocuments} />
    </Page>
  )
}
