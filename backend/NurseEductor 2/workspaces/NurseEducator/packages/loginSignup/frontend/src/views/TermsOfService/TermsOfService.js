import React, {useEffect, useContext, useState} from 'react'
import GlobalContext from "../../context/GlobalContext";
import axios from '../../axiosConfig'


const TermsOfService = () => {
    // const { terms } = useContext(GlobalContext);

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
    console.log(
      "pathname",
      window.location.origin
    );

        axios
        .get(`/${pathName[3]}/${queryString.length > 0 ? '?' + queryString : ''}`)
        .then((response) => {
          
            document.getElementById("terms-data").insertAdjacentHTML('beforeend', response.data.theme_config.terms_of_use);
        });
    }, [])
    
    
  return (
    <div className='w-screen h-screen bg-white relative z-40'>
        <div class="overflow-y-scroll p-4" id="terms-data"></div>
    </div>
  )
}

export default TermsOfService