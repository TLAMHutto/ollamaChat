import React from 'react';
import {
  IconButton,
  SpeedDial,
  SpeedDialHandler,
  SpeedDialContent,
  SpeedDialAction,
} from "@material-tailwind/react";
import {
  PlusIcon,
  HomeIcon,
  CogIcon,
  Square3Stack3DIcon,
} from "@heroicons/react/24/outline";
import GridViewIcon from '@mui/icons-material/GridView';
import { useNavigate } from 'react-router-dom';
import '../pages/styles/SpeedDialButton.css';

export function SpeedDialButton() {
  const navigate = useNavigate();
  const handleClick = (path) => {
    navigate(path);
  };

  return (
    <div className="fixed top-4 left-4 p-4 z-50">
      <SpeedDial placement="bottom-start">
        <SpeedDialHandler className='speed-dial'>
          <IconButton size="lg" className="rounded-full bg-blue-500 text-white">
            <PlusIcon className="h-5 w-5" />
          </IconButton>
        </SpeedDialHandler>
        <SpeedDialContent className="flex items-center gap-2">
          <SpeedDialAction onClick={() => handleClick('/')} className="bg-blue-500 text-white speed-dial-action">
            <HomeIcon className="h-5 w-5" />
          </SpeedDialAction>
          <SpeedDialAction onClick={() => handleClick('/pages/Settings')} className="bg-blue-500 text-white speed-dial-action">
            <CogIcon className="h-5 w-5" />
          </SpeedDialAction>
          <SpeedDialAction onClick={() => handleClick('/pages/Database')} className="bg-blue-500 text-white speed-dial-action">
            <Square3Stack3DIcon className="h-5 w-5" />
          </SpeedDialAction>
          <SpeedDialAction onClick={() => handleClick('/pages/GridView')} className="bg-blue-500 text-white speed-dial-action">
            <GridViewIcon className="h-5 w-5" />
          </SpeedDialAction>
        </SpeedDialContent>
      </SpeedDial>
    </div>
  );
}