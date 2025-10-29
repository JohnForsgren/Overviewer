import { useContext } from 'react'
import { AppContext } from '../../../../utils/appContext'
import ModalSearchWindow from './ModalSearchWindow'

export default function ContainerSearchWindow() {
  const { showSearch, setShowSearch } = useContext(AppContext)
  return (
    <>
      {showSearch && (
        <div className="flex justify-center items-center fixed inset-0 z-40">
          <div
            onClick={() => setShowSearch(false)}
            role="presentation"
            className="absolute inset-0 bg-black bg-opacity-20 transition-opacity backdrop-blur-sm"
          ></div>
          <div className="flex justify-center md:w-4/5 lg:w-3/4 2xl:w-[1200px] px-4 transform transition-all opacity-100 scale-100">
            <ModalSearchWindow />
          </div>
        </div>
      )}
    </>
  )
}
