import { colors } from "./config";

export const styles = {
   chatWidget: {

       position: "fixed",
       bottom: "20px",
       right: "20px",
       backgroundColor: colors.primary,

       paddingLeft: "18px",
       paddingRight: "18px",
       paddingTop: "7px",
       paddingBottom: "7px",

       borderRadius: "10px",
       cursor: "pointer",
   },

  //  modalWindow: {
  //   // Position
  //   position: "fixed",
  //   bottom: "70px",
  //   right: "20px",
  //   // Size
  //   width: "370px",
  //   // width: "420px",
  //   height: "65vh",
  //   maxWidth: "calc(100% - 48px)",
  //   maxHeight: "calc(100% - 48px)",
  //   backgroundColor: "white",
  //   // Border
  //   borderRadius: "12px",
  //   border: `2px solid ${colors.primary}`,
  //   overflow: "visible",
  //   // Shadow
  //   boxShadow: "0px 0px 16px 6px rgba(0, 0, 0, 0.33)",
  // }
}