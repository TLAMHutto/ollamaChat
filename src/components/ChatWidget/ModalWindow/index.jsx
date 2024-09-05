import { styles } from "./../styles";
//for displaying the model view/Window
function ModalWindow(props) {
    // returning display
    return (
        <div
            style={{
                ...styles.modalWindow,
                ...{ opacity: props.visible ? "1" : "0" },

            }}
        >
             <span>Hello there!</span>
        </div>
    );
}
export default ModalWindow;