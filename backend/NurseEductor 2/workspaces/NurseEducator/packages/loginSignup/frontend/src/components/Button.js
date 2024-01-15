import React from 'react'

const Button = ({label, styleClass, onClick, disabled}) => {
  return (
    <button onClick={onClick} disabled={disabled} class={`text-white w-full font-bold bg-primary border-0 py-3 px-8 mt-4 text-base ${styleClass} ${disabled ? 'opacity-60' : 'opacity-100'}`}>
            {label}
          </button>
  )
}

export default Button