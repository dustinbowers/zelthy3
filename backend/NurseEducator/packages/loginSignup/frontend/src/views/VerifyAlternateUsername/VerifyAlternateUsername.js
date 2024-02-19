import React, { useState, useEffect, useContext } from "react";
import Button from "../../components/Button";

import GlobalContext from "../../context/GlobalContext";
import axios from "../../axiosConfig";
import { useNavigate } from "react-router-dom";
import Card from "../../components/Card";
import { convertToHtml } from "../../utils/helper";

const VerifyEmail = () => {
  const [counter, setCounter] = useState(30);
  const [altUsrName, setAltUsrName] = useState()
  const navigate = useNavigate();

  const {
    alternateUsername,
    setAlternateUsername,
    requestId,
    useExist,
    consentText,
    otp,
    username,
    setAlternateOTP,
    logoUrl,
    headerText,
    paraText,
    setErrorMsg,
    canSkipAltUsrName,
    altUsrType,
    baseUrl,
    errorMsg,
    setAltUsrType,
    countryCode,
    usrNameTypes,
    mobileLogo
  } = useContext(GlobalContext);

  const updateUsername = (val) => {
    setAlternateUsername(val);
    setAltUsrName(val)
  };

  const getOTP = () => {
    let usr 
    if (usrNameTypes.includes("email") && usrNameTypes.includes("mobile")) {
      usr = username
    } else if(usrNameTypes.includes("email")){
      usr = username
    } else if(usrNameTypes.includes("mobile")){
      usr = countryCode + username
    }

    let postData = {
      step: "verify_alternate_username",
      request_id: requestId,
      username: usr,
      alternate_username: altUsrName,
      otp: otp,
    };

    if(altUsrType === "mobile"){
      postData.alternate_username = countryCode + alternateUsername
    } else {
      postData.alternate_username = alternateUsername
    }  


    if (!useExist) {
      postData.consent_text = consentText;
    }
    if (altUsrType === "email") {
      if (!validateEmail(alternateUsername)) {
        setErrorMsg("Enter Valid Email");
        return;
      }
    }

    axios
      .post(baseUrl, postData)
      .then((response) => {
        console.log("login response data", response);
        if (response.data.next === "send_alternate_username_otp") {
          sendAlternateOtp();
          setAlternateOTP(true);
          // navigate("/verify-otp");
        } else {
          // setCallConsentOnPage(response.data.on_username_page);
          // setUseExist(false);
          // navigate("/signup");
        }
      })
      .catch((error) => {
        setErrorMsg(error.response.data.message);
      });
    console.log("get otp", alternateUsername);
  };

  const validateEmail = (email) => {
    return email.match(
      /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    );
  };

  const sendAlternateOtp = () => {
    let usr 
    if (usrNameTypes.includes("email") && usrNameTypes.includes("mobile")) {
      usr = username
    } else if(usrNameTypes.includes("email")){
      usr = username
    } else if(usrNameTypes.includes("mobile")){
      usr = countryCode + username
    }

    let postData = {
      step: "send_alternate_username_otp",
      request_id: requestId,
      // "username": "rajat1234@zelthy.com",
      username: usr,
      alternate_username: alternateUsername,
    };
    if (!useExist) {
      postData.consent_text = consentText;
    }

    axios.post(baseUrl, postData).then((response) => {
      console.log("response data", response);
      if (response.data.next === "verify_alternate_username_otp") {
        setAltUsrType("email")
        // console.log("send alt otp data", response.data)
        navigate("/verify-otp");
      }
    });
  };

  const skipStep = () => {
    let usr 
    if (usrNameTypes.includes("email") && usrNameTypes.includes("mobile")) {
      usr = username
    } else if(usrNameTypes.includes("email")){
      usr = username
    } else if(usrNameTypes.includes("mobile")){
      usr = countryCode + username
    }

    let postData = {
      step: "skip_alternate_username",
      request_id: requestId,
      username: usr,
      otp: otp,
    };
    if (!useExist) {
      postData.consent_text = consentText;
    }

    axios
      .post(baseUrl, postData)
      .then((response) => {
        console.log("skip step response data", response);
        if (response.data.next === "done") {
          window.location.href = "/app/home/";
        }
      })
      .catch((error) => {
        setErrorMsg(error.response.data.message);
      });
  };

  useEffect(() => {
    if (counter !== 0) {
      const timer =
        counter > 0 && setInterval(() => setCounter(counter - 1), 1000);
      return () => clearInterval(timer);
    }
  }, [counter]);

  useEffect(() => {
    setErrorMsg("");
  }, []);

  return (
    <>
      <section className="h-full">
        <div className="md:container xl:px-16 md:mx-auto flex flex-wrap justify-between w-screen items-center md:h-full flex-col sm:flex-row">
          <div className="w-full hidden md:block lg:w-5/12 md:w-1/2 pr-0 text-center md:text-left text-white">
            <h1 class="title-font text-4xl ">{convertToHtml(headerText)}</h1>
            <p class="leading-relaxed mt-4 text-lg">{convertToHtml(paraText)}</p>
          </div>
          {/* <div className="md:w-1/2 w-screen text-center pl-0 lg:pl-36 xl:pl-56"> */}
            <Card logoUrl={logoUrl} mobileLogo={mobileLogo} title="Alternate Username">
              <div className="relative mb-4 mt-6">
                <label
                  for="full-name"
                  className="leading-6 text-xl font-bold"
                >
                  {altUsrType === "mobile" ? "Mobile Number" : "Email"}
                </label>
               

                {altUsrType === "mobile" ? 
                <div className="input-box border border-[#D4D4D4] mt-6">
                <span class="prefix">{countryCode}</span> 
                <input
                  type="text"
                  id="username"
                  name="username"
                  onChange={(e) => updateUsername(e.target.value)}
                  value={alternateUsername}
                  placeholder={`Enter ${
                    altUsrType === "mobile" ? "Mobile Number" : "Email"
                  }`}
                  className="w-full bg-boxBg rounded border border-gray text-base outline-none text-gray-700 py-2 px-3 leading-8 transition-colors duration-200 ease-in-out"
                />
              </div>
              : <div className="input-box border border-[#D4D4D4] mt-6">
              <input
                type="email"
                id="username"
                name="username"
                onChange={(e) => updateUsername(e.target.value)}
                value={alternateUsername}
                placeholder={`Enter ${
                  altUsrType === "mobile" ? "Mobile Number" : "Email"
                }`}
                className="w-full bg-boxBg rounded border border-gray text-base outline-none text-gray-700 py-2 px-3 leading-8 transition-colors duration-200 ease-in-out"
              />
            </div>}

                                
                


                {/* <input
                  type="email"
                  id="username"
                  name="username"
                  onChange={(e) => updateUsername(e.target.value)}
                  value={alternateUsername}
                  placeholder={`Enter ${
                    altUsrType === "mobile" ? "Mobile Number" : "Email"
                  }`}
                  className="w-full bg-boxBg rounded border border-gray text-base outline-none text-gray-700 py-2 px-3 mt-8 leading-8 transition-colors duration-200 ease-in-out"
                /> */}
              </div>
              {errorMsg.length > 2 && (
                <div className="text-errorText  text-sm md:bg-white opacity-70">
                  {errorMsg}
                </div>
              )}

<div className="absolute w-full bottom-0 mx-auto text-center">
              <Button label="Get One Time Pin" onClick={getOTP} />
              
              {canSkipAltUsrName && (
                <button
                  onClick={skipStep}
                  className="text-primary cursor-pointer text-center mt-2"
                >
                  Skip
                </button>
              )}
              </div>
            </Card>
          </div>
        {/* </div> */}
      </section>
    </>
  );
};

export default VerifyEmail;
