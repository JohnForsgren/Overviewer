import axios from 'axios'
import { BaseUrl } from '../../utils/api'

export const QuerySearch = async (
  val: string,
  searchAllManuals: number | undefined,
  pdfTextSearch: boolean
) => {
  const res = await axios.get(
    BaseUrl +
      '/query?searchTerm=' +
      val +
      '&searchOnManual=' +
      searchAllManuals +
      '&indexedFiles=' +
      pdfTextSearch
  )

  return res.data
}
