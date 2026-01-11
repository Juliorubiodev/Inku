import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'

const rootElement = document.getElementById('root');
if (rootElement) {
  try {
    createRoot(rootElement).render(
      <StrictMode>
        <App />
      </StrictMode>,
    );
  } catch (error) {
    console.error('Failed to render app:', error);
    rootElement.innerHTML = `<div style="color:red;padding:2rem;">Error: ${error}</div>`;
  }
} else {
  console.error('Root element not found');
}
