// @ts-nocheck
// UAT example (Page). Non-operational stub included for parsing tests.
import { useState } from 'react'
import Breadcrumbs from '../features/breadcrumbs/components/breadcrumbs'
import Header from '../features/header/components/Header'
import SideNav from '../features/sidenav/components/SideNav'
import Footer from './Footer'

type props = {
  children: any
}
export default function Page({ children }: props) {
  const [collapsed, setCollapsed] = useState(false)
  return (
    <>
      <div className={`${collapsed ? 'lg:pl-20' : 'lg:pl-80 2xl:pl-96'}`}>
        <Header collapsed={collapsed} />
      </div>
      <SideNav collapsed={collapsed} setCollapsed={setCollapsed} />
      <div
        className={`${collapsed ? 'lg:pl-20' : 'lg:pl-80 2xl:pl-96'} lg:pt-16`}
      >
        <div className="px-1 md:px-4">
          <div className="w-full h-full rounded-lg">
            <Breadcrumbs className="hidden sm:flex mb-3 w-5/5 ml-2" />
            {children}
          </div>
          <div className="my-8" />
        </div>
      </div>
      <Footer collapsed={collapsed} />
    </>
  )
}
