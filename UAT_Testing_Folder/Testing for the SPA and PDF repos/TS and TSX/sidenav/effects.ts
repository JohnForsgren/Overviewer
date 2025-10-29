// @ts-nocheck
// UAT example (sidenav/effects). Suppress TS diagnostics.
import axios from 'axios'
import { BaseUrl } from '../../utils/api'

export const getInitialStructure = async (manualId: string | undefined) => {
  if (manualId === undefined) return
  const res = await axios.get(BaseUrl + '/navigation?id=' + manualId)
  return res.data
}

export const getAllParts = async (manualId: string | undefined) => {
  if (manualId === undefined) return
  const res = await axios.get(BaseUrl + '/item?type=Part&manualId=' + manualId)
  return res.data
}

export const getAllDocuments = async (manualId: string | undefined) => {
  if (manualId === undefined) return
  const res = await axios.get(
    BaseUrl + '/item?type=Document&manualId=' + manualId
  )
  return res.data
}

export const getAllDesigns = async (manualId: string | undefined) => {
  if (manualId === undefined) return
  const res = await axios.get(
    BaseUrl + '/item?type=Design&manualId=' + manualId
  )
  return res.data
}

export const getTableOfContents = async (manualId: string | undefined) => {
  if (manualId === undefined) return
  const res = await axios.get(BaseUrl + '/item?id=' + manualId)
  return res.data
}
