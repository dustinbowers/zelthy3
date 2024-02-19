// import Header from "./components/Header";
import { useContext, useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
// import celltrionBG from "../assets/celltrionBg.png"
import GlobalContext from "../context/GlobalContext";
import Modal from "../components/modal";
import { convertToHtml } from "../utils/helper";

const hOCLayout =
  (Children) =>
  ({ ...props }) => {
    const { bgImgUrl, logoUrl, privacy, terms, isLogoInBox, footerText, privacyPolicyLink,
      termConditionLink } =
      useContext(GlobalContext);
    const [termModalOpen, setTermModalOpen] = useState(false);
    const [privacyModalOpen, setPrivacyModalOpen] = useState(false);

    const navigate = useNavigate();

    const onLogoClick = () => {
      console.log("on logo click",window.location.hostname)
      window.location = "https://" + window.location.hostname
    }

    // useEffect(() => {
    //   document
    //     .getElementById("footer-text")
    //     .insertAdjacentHTML("beforeend", footerText);
    // }, [footerText]);

    const openLink = (link) => {
      window.open(link, '_blank');
      // window.location = link
    }

    return (
      <>
        <div className="flex flex-col relative h-screen">
          <div class="absolute inset-0 bg-gray-300 z-2 overflow-hidden w-full h-full" onClick={() => onLogoClick()} >
            <img src={bgImgUrl} alt="bgImage" className="h-screen w-screen" />
            <div className="absolute top-0 w-screen h-screen bg-bgColor opacity-[0.87]"></div>
          </div>
          {isLogoInBox ? (
            ""
          ) : (
            <div className="absolute top-6 left-12 cursor-pointer z-30 hidden md:block" onClick={() => onLogoClick()}>
              <img
                src={logoUrl}
                alt="logo"
                className="d-block mx-auto cursor-pointe"
                onClick={() => navigate("/")}
              />
            </div>
          )}

          <div className="h-[calc(100%-40px)] relative z-12">
            <Children {...props} />
          </div>
          {/* <div className="h-[50px] leading-[50px] text-center z-[11]">
         
          {errorMsg.length > 2 && (
            <div className="bg-error md:bg-white opacity-70">{errorMsg}</div>
          )}
        </div> */}
          <div className="h-[40px] bg-white z-[13] text-[#212429] text-xs flex justify-center items-center divide-x">
            {termConditionLink ? <div
              className="px-4 self-center cursor-pointer"
              onClick={() => openLink(termConditionLink)}
            >
              Terms of Use
            </div> : <div
              className="px-4 self-center cursor-pointer"
              onClick={() => setTermModalOpen(true)}
            >
              Terms of Use
            </div> }
            {privacyPolicyLink ? <div
              className="px-4 self-center cursor-pointer"
              onClick={() => openLink(privacyPolicyLink)}
            >
              Privacy Policy
            </div> : <div
              className="px-4 self-center cursor-pointer"
              onClick={() => setPrivacyModalOpen(true)}
            >
              Privacy Policy
            </div>}
          </div>

          <Modal
            modelopen={termModalOpen}
            setmodel={setTermModalOpen}
            data={terms}
          />
          <Modal
            modelopen={privacyModalOpen}
            setmodel={setPrivacyModalOpen}
            data={privacy}
          />
        </div>
        {convertToHtml(footerText, "relative text-center bg-white z-20 px-8 md:px-64 py-2")}
        {/* <div
          className="relative text-center bg-white z-20 px-8 md:px-64 py-2"
          id="footer-text"
        ></div> */}
      </>
    );
  };

export default hOCLayout;
