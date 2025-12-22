import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom';
import { MantineProvider } from '@mantine/core'
import { Notifications } from '@mantine/notifications';

import RoutesApp from './routes'

import '@mantine/core/styles.css';
import '@mantine/notifications/styles.css';

import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';

import './index.css'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <MantineProvider withGlobalStyles withNormalizeCSS>
      <Notifications position="bottom-right" autoClose={3000}/> 
        <BrowserRouter>
          <RoutesApp />
        </BrowserRouter>
    </MantineProvider>
  </StrictMode>,
)
