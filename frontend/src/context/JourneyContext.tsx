import { createContext, useContext, useState } from 'react';

const JourneyContext = createContext<any>(null);

export function JourneyProvider({ children }: { children: any }) {
  const [state, setState] = useState({});
  return (
    <JourneyContext.Provider value={{ state, setState }}>
      {children}
    </JourneyContext.Provider>
  );
}

export function useJourney() {
  return useContext(JourneyContext);
}
