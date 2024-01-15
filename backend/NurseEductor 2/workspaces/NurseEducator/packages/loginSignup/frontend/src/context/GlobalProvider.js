import GlobalContext from "./GlobalContext";
import React, { useState } from "react";

const GlobalProvider = ({ children }) => {
  const [username, setUsername] = useState("");
  const [alternateUsername, setAlternateUsername] = useState("");
  const [requestId, setRequestId] = useState("");
  const [callConsentOnPage, setCallConsentOnPage] = useState(false);
  const [useExist, setUseExist] = useState(false);
  const [consentText, setConsentText] = useState("");
  const [otp, setOtp] = useState();
  const [alternateOTP, setAlternateOTP] = useState(false);
  const [cusrID, setCusrID] = useState();
  const [bgImgUrl, setBgImgUrl] = useState("");
  const [logoUrl, setLogoUrl] = useState("");
  const [headerText, setHeaderText] = useState("");
  const [paraText, setParaText] = useState("");
  const [errorMsg, setErrorMsg] = useState("");
  const [privacy, setPrivacy] = useState("");
  const [terms, setTerms] = useState("");
  const [canSkipAltUsrName, setCanSkipAltUsrName] = useState(false);
  const [altUsrType, setAltUsrType] = useState("phone");
  const [baseUrl, setbaseUrl] = useState("");
  const [usrNameTypes, setUsrNameTypes] = useState("");
  const [loginSignupLabel, setLoginSignupLabel] = useState("");
  const [countryCode, setCountryCode] = useState("+61");
  const [isLogoInBox, setIsLogoInBox] = useState(false);
  const [footerText, setFooterText] = useState("");
  const [mobileLogo, setMobileLogo] = useState("");
  const [privacyPolicyLink, setPrivacyPolicyLink] = useState();
  const [termConditionLink, setTermConditionLink] = useState();

  return (
    <GlobalContext.Provider
      value={{
        setUsername,
        username,
        requestId,
        setRequestId,
        callConsentOnPage,
        setCallConsentOnPage,
        useExist,
        setUseExist,
        consentText,
        setConsentText,
        alternateUsername,
        setAlternateUsername,
        otp,
        setOtp,
        alternateOTP,
        setAlternateOTP,
        cusrID,
        setCusrID,
        bgImgUrl,
        setBgImgUrl,
        logoUrl,
        setLogoUrl,
        headerText,
        setHeaderText,
        paraText,
        setParaText,
        errorMsg,
        setErrorMsg,
        privacy,
        setPrivacy,
        terms,
        setTerms,
        canSkipAltUsrName,
        setCanSkipAltUsrName,
        altUsrType,
        setAltUsrType,
        baseUrl,
        setbaseUrl,
        setUsrNameTypes,
        usrNameTypes,
        loginSignupLabel,
        setLoginSignupLabel,
        countryCode,
        setCountryCode,
        isLogoInBox,
        setIsLogoInBox,
        footerText,
        setFooterText,
        setMobileLogo,
        mobileLogo,
        privacyPolicyLink,
        setPrivacyPolicyLink,
        termConditionLink,
        setTermConditionLink,
      }}
    >
      {children}
    </GlobalContext.Provider>
  );
};

export default GlobalProvider;
