import { useState } from 'react'
import Table from '../../table/components/Table'
import SearchInput from './SearchInput'

type props = {
  query?: string
  category?: string
}

export default function SearchWindow({ query, category }: props) {
  const [result, setResult] = useState<any>(() => [])
  return (
    <div className="bg-white rounded-xl mt-2">
      <div className="flex flex-col">
        <SearchInput category={category} query={query} setResult={setResult} />
        <div className="">
          <Table incomingData={result} />
        </div>
      </div>
    </div>
  )
}
