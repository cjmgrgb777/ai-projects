import React from 'react'

const App = () => {
  
  const bg = "231F20";
  const primary = "0B7A75";
  const white = "F0EFF4"

  return (
    <div className={`h-screen`}>
      <header className={`bg-[#${primary}] p-4 font-bold text-[#${white}]`}>
        <h3 className='text-3xl'>ChatBot</h3>
      </header>
      {/* ABOUT */}
      <div className='p-4'>
        <h1 className={`font-bold text-3xl`}>About</h1>
        <p></p>
      </div>
    </div>
  )
}

export default App