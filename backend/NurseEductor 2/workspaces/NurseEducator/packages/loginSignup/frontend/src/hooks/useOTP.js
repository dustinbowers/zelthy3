import { useState } from "react";
export default function useOTP(init, callback) {
  const [values, setValues] = useState(init);
  const [current, setCurrent] = useState(0);

  const handleKeyUp = (e, index) => {
    if (e.key === "Backspace") {
      setCurrent(index - 1);
    }
  };

  const handleChange = (e, index) => {
    const { value, name } = e.target;
    if (isNaN(value)) return;

    setValues((values) => {
      if (!value) setCurrent(index);
      else setCurrent(index + 1);

      return {
        ...values,
        [name]: value[value.length - 1] ?? ""
      };
    });
  };

  return {
    values,
    handleChange,
    current,
    handleKeyUp
  };
}
