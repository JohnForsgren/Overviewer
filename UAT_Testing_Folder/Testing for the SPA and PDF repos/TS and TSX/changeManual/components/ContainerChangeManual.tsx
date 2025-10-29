import { useContext } from 'react'
import { AppContext } from '../../../utils/appContext'
import ChangeManualModal from './ChangeManualModal'

export default function ContainerChangeManual() {
  const { showChangeManual, setShowChangeManual } = useContext(AppContext)
  return (
    <>
      {showChangeManual && (
        <div className="flex justify-center items-center fixed inset-0 z-40">
          <div
            onClick={() => setShowChangeManual(false)}
            role="presentation"
            className="absolute inset-0 bg-black bg-opacity-20 backdrop-blur-sm"
          ></div>
          <div className="flex justify-center relative max-h-[80%] 2xl:mb-0">
            <ChangeManualModal />
          </div>
        </div>
      )}
    </>
  )
}
