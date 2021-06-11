import * as React from "react";
import styles from "./AbcLicCheck.module.scss";
import { IAbcLicCheckProps } from "./IAbcLicCheckProps";
import { escape } from "@microsoft/sp-lodash-subset";
import { PropertyPaneSlider } from "@microsoft/sp-property-pane";
import { PrimaryButton } from "office-ui-fabric-react";

const Navigation = ({ handlePageButton, handleOptionButton, state }) => {
  return (
    <div className={styles.nav}>
      <div className={styles.pageButtons}>
        <PrimaryButton
          onClick={() => handlePageButton("dashboard")}
          id={state.currentPage == "dashboard" ? styles.selectedPage : ""}
          className="rectangle"
        >
          Dashboard
        </PrimaryButton>
        {GetPageButtons(handlePageButton, state)}
      </div>
      <div className={styles.optionsButtons}>
        <PrimaryButton onClick={() => handleOptionButton()} id={styles.optionsButton}>
          ⚙️
        </PrimaryButton>
        {state.menuOpen ? GetOptionMenu(handlePageButton, state) : ""}
      </div>
    </div>
  );
};

function GetPageButtons(handlePageButton: Function, state) {

  const buttons = state.pages.map((report) => {
    return (
      <PrimaryButton
        onClick={() => handlePageButton(report.name)}
        id={state.currentPage == report.name ? styles.selectedPage : ""}
        key={report.name.trim()}
        className={`rectangle ${styles.pageButton}`}
      >
        {report.formalName}
      </PrimaryButton>
    );
  });

  return buttons;
}

function GetOptionMenu(handlePageButton: Function, state) {

  function getOptions(options: Array<any>) {
    let optionsHTML = options.map((option) => {
      return (
        <li
          className={styles.optionItem}
          onClick={() => handlePageButton(option.name)}
        >
          {option.formalName}
        </li>
      );
    });

    return optionsHTML;
  }

  return (
    <div className={styles.optionMenu}>
      <ul className={styles.optionList}>{getOptions(state.options)}</ul>
    </div>
  );
}

export default Navigation;
