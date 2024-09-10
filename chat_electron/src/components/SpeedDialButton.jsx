import {
    IconButton,
    SpeedDial,
    SpeedDialHandler,
    SpeedDialContent,
    SpeedDialAction,
    Typography,
  } from "@material-tailwind/react";
  import {
    PlusIcon,
    HomeIcon,
    CogIcon,
    Square3Stack3DIcon,
  } from "@heroicons/react/24/outline";
  import { useNavigate } from 'react-router-dom'


  export function SpeedDialButton() {
    const labelProps = {
      variant: "small",
      color: "white",
      className:
      "absolute top-2/4 -right-0 -translate-y-2/4 -translate-x-1/15 font-normal side-text",
    };

    const navigate = useNavigate()
    const handleClick = (path) => {
      navigate(path);
    };

    return (
      <div className="fixed top-4 left-4 p-4">
      <SpeedDial>
        <SpeedDialHandler>
          <IconButton size="lg" className="rounded-full">
            <PlusIcon className="h-5 w-5 transition-transform group-hover:rotate-45" />
          </IconButton>
        </SpeedDialHandler>
        <SpeedDialContent>
          <SpeedDialAction onClick={() => handleClick('/')} className="flex items-center">
            <HomeIcon className="h-5 w-5" />
          </SpeedDialAction>
          <SpeedDialAction onClick={() => handleClick('/pages/Settings')} className="flex items-center">
            <CogIcon className="h-5 w-5" />
          </SpeedDialAction>
          <SpeedDialAction className="flex items-center" onClick={() => handleClick('/pages/Database')}>
            <Square3Stack3DIcon className="h-5 w-5" />
          </SpeedDialAction>
        </SpeedDialContent>
      </SpeedDial>
    </div>
    
    );
  }
  