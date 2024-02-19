import React, { useContext, useEffect } from "react";
import Button from "../../components/Button";
import axios from "../../axiosConfig";
import { useNavigate } from "react-router-dom";
import GlobalContext from "../../context/GlobalContext";
import Card from "../../components/Card";
import { convertToHtml } from "../../utils/helper";

const Login = () => {
  const navigate = useNavigate();
  const {
    username,
    setUsername,
    requestId,
    setCallConsentOnPage,
    setUseExist,
    logoUrl,
    headerText,
    paraText,
    setErrorMsg,
    baseUrl,
    errorMsg,
    usrNameTypes,
    loginSignupLabel,
    setConsentText,
    countryCode,
    mobileLogo
  } = useContext(GlobalContext);

  const updateUsername = (val) => {
    setUsername(val);
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

    console.log("user name type available", usrNameTypes)

    let postData = {
      step: "verify_username",
      request_id: requestId,
      // "username": "rajat1234@zelthy.com",
      username: usr,
    };
    axios
      .post(baseUrl, postData)
      .then((response) => {
        console.log("login response data", response);
        if (response.data.next === "send_login_otp") {
          sendOtp();
          // navigate('/verify-otp')
        } else {
          setCallConsentOnPage(response.data.on_username_page);
          setUseExist(false);
          setConsentText(response.data.consent_text);
          navigate("/signup");
        }
      })
      .catch((error) => {
        setErrorMsg(error.response.data.message);
      });
    console.log("get otp", username);
  };

  const sendOtp = () => {
    let postData = {
      step: "send_login_otp",
      request_id: requestId,
      // "username": "rajat1234@zelthy.com",
      username: username,
    };
    setUseExist(true);
    axios
      .post(baseUrl, postData)
      .then((response) => {
        console.log("response data", response);
        if (response.data.next === "verify_login_otp") {
          navigate("/verify-otp");
        }
      })
      .catch((error) => {
        setErrorMsg(error.response.data.message);
      });
  };

  useEffect(() => {
    setErrorMsg("");
    console.log("allowd user", loginSignupLabel);
  }, []);

  return (
    <section className="h-full w-full">
      {usrNameTypes && (
        <div className="md:container md:px-8 xl:px-16 md:mx-auto flex flex-wrap justify-between w-screen items-center md:h-full flex-col sm:flex-row">
          <div className="w-full hidden md:block lg:w-5/12 md:w-1/2 pr-0 text-center md:text-left text-white">
            <h1 class="title-font text-4xl ">{convertToHtml(headerText)}</h1>
            <p class="leading-relaxed mt-4 text-lg">{convertToHtml(paraText)}</p>
          </div>
          {/* <div className="md:w-1/2 w-screen text-center pl-0 lg:pl-32 xl:pl-48 overflow-hidden md:overflow-auto"> */}
          <Card logoUrl={logoUrl} mobileLogo={mobileLogo} title="Log in">
            <div className="relative mt-10">
              <label for="full-name" className="leading-6 text-xl font-bold">
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
                  onChange={(e) => updateUsername(e.target.value)}
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
                  onChange={(e) => updateUsername(e.target.value)}
                  value={username}
                  className="w-full bg-boxBg text-base outline-none px-3 leading-8 transition-colors duration-200 ease-in-out"
                />
              </div> : usrNameTypes.includes("email") ? <div className="input-box border border-[#D4D4D4] mt-6">
                <input
                  type="text"
                  id="username"
                  name="username"
                  placeholder="example@mail.com"
                  onChange={(e) => updateUsername(e.target.value)}
                  value={username}
                  className="w-full bg-boxBg text-base outline-none px-3 leading-8 transition-colors duration-200 ease-in-out"
                />
              </div> : "" }

              


            </div>
            {errorMsg?.length > 2 && (
              <div className="text-errorText text-sm md:bg-white opacity-70">
                {errorMsg}
              </div>
            )}

            <div className="absolute w-full bottom-0 mx-auto">
              <Button
                label="Get One Time Pin"
                onClick={getOTP}
                disabled={username.length > 0 ? false : true}
              />
            </div>
            {/* <div className="flex flex-row items-center justify-left text-sm font-medium space-x-1 mt-3">
                <p>Forgot Password?</p> <a className="flex flex-row items-center font-semibold text-primary" href="http://" target="_blank" rel="noopener noreferrer">Click Here</a>
              </div> */}
          </Card>
          {/* </div> */}
        </div>
      )}
    </section>
  );
};

export default Login;
