// importing external style
import { styles } from "./styles";
// import icon
import { BsFillChatFill } from "react-icons/bs";
import { useEffect, useRef, useState } from "react";
//import ModalWindow
import ModalWindow from "./ModalWindow";




function ChatWidget() {
    // state variable to track if widget button was hovered on
    const [hovered, setHovered] = useState(false);
    // state variable to track modal visibility
    const [visible, setVisible] = useState(false);
    //creating a ref 'id'
    const widgetRef = useRef(null);
    // use effect listener to check if the mouse was cliked outside the window 
    useEffect(() => {
        function handleClickOutside(event) {
            if (widgetRef.current && !widgetRef.current.contains(event.target)) {
                setVisible(false);
            }
        }
        document.addEventListener("mousedown", handleClickOutside);
        return () => {
            document.removeEventListener("mousedown", handleClickOutside);
        };
    }, [widgetRef]);

    return (
        //container
        //call widgetRef inside the div
        <div ref={widgetRef}>
            {/* Call Modal Window */}
            <ModalWindow visible={visible} />

            {/* Chat Button Component */}
            <div
                onClick={() => setVisible(!visible)}
                onMouseEnter={() => setHovered(true)}
                onMouseLeave={() => setHovered(false)}
                style={{
                    ...styles.chatWidget,
                    ...{ border: hovered ? "1px solid black" : "" },
                }}
            >
                {/* Inner Container */}
                <div
                    style={{
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                    }}
                >
                    {/* Button Icon */}
                    <BsFillChatFill size={20} color="white" />

                    {/* Button Text */}
                    <span style={styles.chatWidgetText}>Chat Now!!</span>
                </div>
            </div>
        </div>
    );
}


export default ChatWidget;