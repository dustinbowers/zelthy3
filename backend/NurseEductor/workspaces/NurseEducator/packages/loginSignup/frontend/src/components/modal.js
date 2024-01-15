import React, { useEffect } from "react";

const Modal = ({ modelopen, setmodel, data }) => {
    useEffect(() => {
        if (modelopen) {
           
        document.getElementById("model-data").insertAdjacentHTML('beforeend', data);
        }
        
    }, [modelopen])
    
  return (
    <>
      {modelopen && (
        <div
          id="modal"
          class="fixed z-50 inset-0 bg-gray-900 bg-opacity-60 overflow-hidden h-full w-full"
        >
          <div className="absolute z-[5] bg-black opacity-20 w-screen h-screen"></div>

          <div className="pt-12 h-full">

          <div class="relative w-full h-full z-10 shadow-xl rounded-xl bg-white overflow-auto">
            <div class="flex justify-between absolute right-1 items-center text-black text-xl rounded-t-md px-4 py-2">
              <button onClick={() => setmodel(false)}>x</button>
            </div>

            <div class="overflow-y-scroll overflow-x-hidden p-16" id="model-data">
              
            </div>
          </div>
          </div>
        </div>
      )}
    </>
  );
};

export default Modal;
