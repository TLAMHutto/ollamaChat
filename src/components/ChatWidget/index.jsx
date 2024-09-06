import { styles } from "./styles";
import { BsChatSquareText } from "react-icons/bs";
import { useEffect, useRef, useState } from "react";
import ModalWindow from "./ModalWindow";

function ChatWidget({ selectedAiModel }) {
    const [hovered, setHovered] = useState(false);
    const [visible, setVisible] = useState(false);
    const widgetRef = useRef(null);

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
        <div ref={widgetRef}>
            <ModalWindow visible={visible} selectedAiModel={selectedAiModel} />

            <div
                onClick={() => setVisible(!visible)}
                onMouseEnter={() => setHovered(true)}
                onMouseLeave={() => setHovered(false)}
                style={{
                    ...styles.chatWidget,
                    ...{ border: hovered ? "1px solid black" : "" },
                }}
            >
                <div
                    style={{
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                    }}
                >
                    <BsChatSquareText size={20} color="white" />
                </div>
            </div>
        </div>
    );
}

export default ChatWidget;