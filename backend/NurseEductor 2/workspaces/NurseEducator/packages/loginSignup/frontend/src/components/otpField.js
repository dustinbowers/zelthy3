import { useEffect, useRef } from "react";

export default function OTPField({ onChange, onKeyUp, value, name, isFocus }) {
  const inputRef = useRef();
  useEffect(() => {
    if (isFocus) {
      inputRef.current.focus();
    }
  }, [isFocus]);
  return (
    <input
      ref={inputRef}
      className="text-center py-2 w-11 h-14 outline-none border border-gray text-lg bg-white focus:ring-1 ring-primary"
      type="text"
      inputMode="numeric"
      value={value}
      onChange={onChange}
      onKeyUp={onKeyUp}
      name={name}
      autoComplete="off"
    />
  );
}
