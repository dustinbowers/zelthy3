import React from 'react'
import { ReactComponent as Logo } from "../../assets/Zelthy.svg";

const Header = () => {
  const onLogoClick = ()=> {
    console.log("href", window.location.href)
  }
  return (
    <div className="sticky top-0 w-full z-50">
        <div className="mx-auto px-8">
          <div className="flex items-center justify-between h-16">
            <div className=" flex items-center gap-2">
              <a className="flex-shrink-0" href='#void' onClick={onLogoClick} >
                <Logo className="h-5 w-16" />
              </a>
            </div>

           
          </div>
        </div>
    </div>
  )
}

export default Header