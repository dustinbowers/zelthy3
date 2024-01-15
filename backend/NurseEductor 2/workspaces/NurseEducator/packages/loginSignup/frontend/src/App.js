import "./App.css";
import {
  Routes,
  HashRouter as Router,
  Route,
  useNavigate,
  // Navigate,
} from "react-router-dom";
import hOCLayout from "./Layout/HOCLayout";
import Login from "./views/Login/Login";
import Consent from "./views/Consent/Consent";
import OTP from "./views/Otp/OTP";
import VerifyAlternateUsername from "./views/VerifyAlternateUsername/VerifyAlternateUsername";
import Signup from "./views/Signup/Signup";
import { useContext, useEffect, useCallback } from "react";
import axios from "./axiosConfig";
import GlobalContext from "./context/GlobalContext";
import { Toaster } from "react-hot-toast";
import TermsOfService from "./views/TermsOfService/TermsOfService";
import Privacy from "./views/Privacy/Privacy";

function App() {
  const {
    setBgImgUrl,
    setLogoUrl,
    setHeaderText,
    setParaText,
    setRequestId,
    setPrivacy,
    setTerms,
    setbaseUrl,
    setUsrNameTypes,
    setLoginSignupLabel,
    setCountryCode,
    setIsLogoInBox,
    setFooterText,
    setMobileLogo,
    setPrivacyPolicyLink,
    setTermConditionLink,
  } = useContext(GlobalContext);

  const navigate = useNavigate();

  useEffect(() => {
    const urlSearchParams = new URLSearchParams(window.location.search);
    const params = Object.fromEntries(urlSearchParams.entries());

    let queryParams = [];
    Object.keys(params).forEach((element) => {
      queryParams.push(element + "=" + params[element]);
    });

    let queryString = "";
    for (let i = 0; i < queryParams.length; i++) {
      const element = queryParams[i];
      queryString += element + "&";
    }

    queryString = queryString.substring(0, queryString.length - 1);
    console.log("query params", queryParams, queryString);

    console.log("addressbar path", window.location.pathname.split("/"));

    let pathName = window.location.pathname.split("/");
    console.log(pathName)
    console.log("pathname", pathName[4] + "/");
    setbaseUrl(pathName[4] + "/");

    axios
      .get(`/${pathName[4]}/${queryString.length > 0 ? "?" + queryString : ""}`)
      .then((response) => {
        localStorage.setItem("reqid", response.data.request_id);
        console.log("allowed usr type", response.data.username_types);
        setUsrNameTypes(response.data.username_types);
        var r = document.querySelector(":root");
        console.log("config data", response);
        setBgImgUrl(response.data.theme_config.bg_img);
        setLogoUrl(response.data.theme_config.logo);
        setHeaderText(response.data.theme_config.header_text);
        setParaText(response.data.theme_config.para_text);
        setRequestId(response.data.request_id);
        setPrivacy(response.data.theme_config.privacy_policy);
        setTerms(response.data.theme_config.terms_of_use);
        setLoginSignupLabel(response.data.theme_config.username_types);
        setCountryCode(response.data.country_code);
        setIsLogoInBox(response.data.theme_config.is_logo_in_box);
        setFooterText(response.data.theme_config.footer_text);
        setMobileLogo(response.data.theme_config.mobile_logo);
        setPrivacyPolicyLink(response.data.theme_config?.privacy_policy_link);
        setTermConditionLink(
          response.data.theme_config?.terms_and_conditions_link
        );
        r.style.setProperty(
          "--primary",
          response.data.theme_config.primary_color
        );
        r.style.setProperty("--bgColor", response.data.theme_config.bg_color);
        r.style.setProperty("--boxBg", response.data.theme_config.box_bg_color);
        r.style.setProperty(
          "--secondary",
          response.data.theme_config.secondary_color
        );

        if (response.data?.redirect_to_login_page) {
          navigate("/");
        }
      });
  }, []);

  return (
    <>
      <Toaster position="top-left" reverseOrder={false} />

      <div className="App text-std tracking-p.2 flex-1 z-10 h-full">
        <div id="loaderLayout" class="loader">
          <div class="loader-spin"></div>
        </div>
        <div className="font-invention-app"></div>
        {/* <Router> */}
        <Routes>
          {/* <Route path="/login" element={<Login />} /> */}
          <Route path="/consent" element={<Consent />} />
          <Route path="/verify-otp" element={<OTP />} />
          <Route
            path="/verify-username"
            element={<VerifyAlternateUsername />}
          />
          <Route path="/signup" element={<Signup />} />
          <Route path="/terms-and-condition" element={<TermsOfService />} />
          <Route path="/privacy-and-policy" element={<Privacy />} />
          <Route path="/" exact element={<Login />} />
        </Routes>
        {/* </Router> */}
      </div>
    </>
  );
}

export default hOCLayout(App);
