import axios from 'axios'
import { BaseUrl } from '../../utils/api'

export const getManuals = async () => {
  const res = await axios.get(BaseUrl + '/root?')
  return res.data
}
