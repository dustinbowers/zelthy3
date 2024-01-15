import React, { useState, useContext, useEffect } from "react";
import Button from "../../components/Button";
import { ReactComponent as Warning } from "../../assets/warning.svg";
// import { ReactComponent as CelltrionLogo } from "../../assets/celltrionLogo.svg";
import axios from "../../axiosConfig";
import { useNavigate } from "react-router-dom";
import GlobalContext from "../../context/GlobalContext";
import Card from "../../components/Card";
import Modal from "../../components/modal";
import { convertToHtml } from "../../utils/helper";


const Signup = () => {
  const [agreement, setAgreement] = useState(false);
  const [termModalOpen, setTermModalOpen] = useState(false);
  const [privacyModalOpen, setPrivacyModalOpen] = useState(false);
  const [consentModalOpen, setConsentModalOpen] = useState(false);
  const navigate = useNavigate();
  const {
    username,
    setUsername,
    callConsentOnPage,
    requestId,
    setConsentText,
    setCusrID,
    logoUrl,
    headerText,
    paraText,
    setErrorMsg,
    baseUrl,
    errorMsg,
    consentText,
    privacy,
    terms,
    countryCode,
    isLogoInBox,
    usrNameTypes,
    mobileLogo,
  } = useContext(GlobalContext);

  const onGetOtp = (val) => {


    let usr 
    if (usrNameTypes.includes("email") && usrNameTypes.includes("mobile")) {
      usr = username
    } else if(usrNameTypes.includes("email")){
      usr = username
    } else if(usrNameTypes.includes("mobile")){
      usr = countryCode + username
    }

    let postData = {
      step: "signup_username",
      request_id: requestId,
      // "username": "rajat1234@zelthy.com",
      username: usr,
    };
    console.log("onconsent page fix agreement", callConsentOnPage)
    if (!agreement && callConsentOnPage) {
      setErrorMsg("Please check Agreement form");
      return;
    }
    axios
      .post(baseUrl, postData)
      .then((response) => {
        console.log("response data", response);
        setConsentText(response.data?.consent_text);
        setCusrID(response.data?.cuser_id);
        submitConsent(response.data?.consent_text);
        // if (callConsentOnPage) {
        //   setConsentText(response.data?.consent_text);
        //   setCusrID(response.data?.cuser_id);
        //   submitConsent(response.data?.consent_text);
        // } else {
        //   navigate("/consent");
        // }
      })
      .catch((error) => {
        setErrorMsg(error.response.data.message);
      });
    console.log("get otp", val, agreement);
  };

  const submitConsent = (consentText) => {
    let usr 
    if (usrNameTypes.includes("email") && usrNameTypes.includes("mobile")) {
      usr = username
    } else if(usrNameTypes.includes("email")){
      usr = username
    } else if(usrNameTypes.includes("mobile")){
      usr = countryCode + username
    }

    let postData = {
      step: "submit_consent",
      request_id: requestId,
      // "username": "rajat1234@zelthy.com",
      username: usr,
      consent_text: consentText,
    };
    axios
      .post(baseUrl, postData)
      .then((response) => {
        console.log("response data", response);
        if (response.data.next === "send_signup_otp") {
          sendOtp(consentText);
        }
      })
      .catch((error) => {
        setErrorMsg(error.response.data.message);
      });
  };

  const sendOtp = (consentText) => {
    let usr 
    if (usrNameTypes.includes("email") && usrNameTypes.includes("mobile")) {
      usr = username
    } else if(usrNameTypes.includes("email")){
      usr = username
    } else if(usrNameTypes.includes("mobile")){
      usr = countryCode + username
    }

    let postData = {
      step: "send_signup_otp",
      request_id: requestId,
      // "username": "rajat1234@zelthy.com",
      username: usr,
      consent_text: consentText,
    };
    axios
      .post(baseUrl, postData)
      .then((response) => {
        console.log("response data", response);
        if (response.data.next === "verify_signup_otp") {
          navigate("/verify-otp");
        }
      })
      .catch((error) => {
        setErrorMsg(error.response.data.message);
      });
  };

  const checkAgreement = (val) => {
    console.log("agr value", val);
    setAgreement(val);
  };

  useEffect(() => {
    setErrorMsg("");
  }, []);

  return (
    <section className="h-full">
      <div className="md:container xl:px-16 md:mx-auto flex flex-wrap justify-between w-screen items-center md:h-full flex-col sm:flex-row">
        <div className="w-full hidden md:block lg:w-5/12 md:w-1/2 pr-0 text-center md:text-left text-white">
          <h1 class="title-font text-4xl ">{convertToHtml(headerText)}</h1>
          <p class="leading-relaxed mt-4 text-lg">{convertToHtml(paraText)}</p>
        </div>
        {/* <div className="md:w-1/2 w-screen text-center pl-0 lg:pl-36 xl:pl-56"> */}

        <Card logoUrl={logoUrl} mobileLogo={mobileLogo} title="Sign Up">
          <div className={`relative  ${isLogoInBox ? "mt-4 mb-4" : "mt-6 mb-5"}`}>
            <label for="full-name" className="leading-6 text-xl font-bold ">
             Enter
             {usrNameTypes.includes("email") && usrNameTypes.includes("mobile")
                    ? " Username"
                    : usrNameTypes.length === 1 &&
                      usrNameTypes.includes("email")
                    ? " Email"
                    : " Mobile Number"}
            </label>

            {usrNameTypes.includes("email") && usrNameTypes.includes("mobile") ? <div className="input-box border border-[#D4D4D4] mt-6">
                <input
                  type="text"
                  id="username"
                  name="username"
                  placeholder="Enter Username"
                  onChange={(e) => setUsername(e.target.value)}
                  value={username}
                  className="w-full bg-boxBg text-base outline-none px-3 leading-8 transition-colors duration-200 ease-in-out"
                />
              </div> : usrNameTypes.includes("mobile") ? <div className="input-box border border-[#D4D4D4] mt-6">
                <span class="prefix">{countryCode}</span>
                <input
                  type="text"
                  id="username"
                  name="username"
                  placeholder="499999999"
                  onChange={(e) => setUsername(e.target.value)}
                  value={username}
                  className="w-full bg-boxBg text-base outline-none px-3 leading-8 transition-colors duration-200 ease-in-out"
                />
              </div> : usrNameTypes.includes("email") ? <div className="input-box border border-[#D4D4D4] mt-6">
                <input
                  type="text"
                  id="username"
                  name="username"
                  placeholder="example@mail.com"
                  onChange={(e) => setUsername(e.target.value)}
                  value={username}
                  className="w-full bg-boxBg text-base outline-none px-3 leading-8 transition-colors duration-200 ease-in-out"
                />
              </div> : ""}


          </div>
          {errorMsg.length > 2 && (
            <div className="text-errorText  text-sm md:bg-white opacity-70">
              {errorMsg}
            </div>
          )}

          {callConsentOnPage && (
            <div className="flex items-center">
              <input
                type="checkbox"
                id="consent-form"
                className="accent-primary w-4 h-4 border rounded mr-2 cursor-pointer"
                name="consent-form"
                onChange={(e) => checkAgreement(e.target.checked)}
                checked={agreement}
              />
              <label
                className="text-xs text-[#757575] ml-2"
                htmlFor="consent-form"
              >
                I agree to the{" "}
                <span
                  className="text-primary font-medium cursor-pointer"
                  onClick={() => setTermModalOpen(true)}
                >
                  Terms of Use
                </span>{" "}
                {consentText.length === 0 ? "and " : ", "}
                <span
                  className="text-primary font-medium cursor-pointer"
                  onClick={() => setPrivacyModalOpen(true)}
                >
                  Privacy Policy
                </span>
                {consentText.length > 1 && " and "}
                {consentText.length > 1 && (
                  <span
                    className="text-primary font-medium cursor-pointer"
                    onClick={() => setConsentModalOpen(true)}
                  >
                    Consent
                  </span>
                )}
                .
              </label>
            </div>
          )}

          <div
            className={`bg-warninBg px-4 ${
              isLogoInBox ? "py-2" : "py-3"
            }  my-4 flex text-warningText text-sm`}
          >
            <Warning className="w-6 h-6 mr-2" />
            <div>
              Please enter a registered {(usrNameTypes.includes("mobile") && usrNameTypes.includes("email")) ? "username" : usrNameTypes.includes("mobile") ? "mobile number" : usrNameTypes.includes("email") && "email"}. If you are a new user,
              proceed with the signup process.
            </div>
          </div>

          <div className="absolute w-full bottom-0 mx-auto">
            <Button
              label="Get One Time Pin"
              onClick={onGetOtp}
              disabled={username.length > 0 ? false : true}
            />
          </div>
          {/* <div className="mt-2 text-[#757575] text-sm">
                Already a user? 
                <span className="text-primary ml-1 font-bold cursor-pointer" onClick={() => navigate("/")}>
                Login
                  </span> 
                </div> */}

          {/* <div className="flex flex-row items-center justify-left text-sm font-medium space-x-1 mt-3">
              <p>Forgot Password?</p> <a className="flex flex-row items-center font-semibold text-primary" href="http://" target="_blank" rel="noopener noreferrer">Click Here</a>
            </div> */}
        </Card>

        {/* </div> */}
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
      <Modal
        modelopen={consentModalOpen}
        setmodel={setConsentModalOpen}
        data={consentText}
      />
    </section>
  );
};

export default Signup;
