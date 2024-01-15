import React, { useContext } from "react";
import GlobalContext from "../context/GlobalContext";

const Card = ({ logoUrl, title, children, mobileLogo }) => {
  const { isLogoInBox } = useContext(GlobalContext);

  return (
    <div className="md:w-1/2 w-screen text-right overflow-hidden md:overflow-auto md:flex md:flex-row-reverse">
      <div className="bg-boxBg p-8 md:w-[450px] flex flex-col text-left h-screen lg:h-[460px] pb-24 md:pb-12 md:mt-0 relative">
        {isLogoInBox && <div
          className={`text-center ${isLogoInBox ? "" : "md:hidden"}  w-full`}
        >
          <img src={logoUrl} alt="logo" className="d-block mx-auto" />
        </div>}
        <div className="text-center w-full lg:hidden">
        <img src={mobileLogo} alt="logo" className="d-block mx-auto" />
        </div>
        <div className="text-gray-900 text-[32px] font-bold title-font mb-1 lg:mt-3">
          Log In
        </div>
        <div className="w-[40px] h-[6px] rounded-lg bg-secondary"></div>
        <div className="relative h-full">{children}</div>
      </div>
    </div>
  );
};

export default Card;
