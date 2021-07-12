import * as React from "react";
import styles from "./styles/Navigation.module.scss";
import { IAbcLicCheckProps } from "./IAbcLicCheckProps";
import { escape } from "@microsoft/sp-lodash-subset";
import { PropertyPaneSlider } from "@microsoft/sp-property-pane";
import { Dropdown, IDropdownOption, IconButton, IIconProps, Label } from "office-ui-fabric-react";

// TODO Add motion slide out menu when button clicked
// TODO Map options to slide out menu

const Navigation = ({
  state,
  setPage,
}) => {
 
  const menuIcon: IIconProps = { iconName: 'CollapseMenu'}

  return (
    <div className={`${styles.nav} ms-Grid-row`}>
      <div className={`${styles.dropdownCtnr} ms-Grid-col ms-sm6 ms-md6 ms-lg4`}>
        <Dropdown 
          className={`${styles.dropdown}`}
          placeholder="Select report..."
          selectedKey={state.currentPage.key} 
          options={state.reports} 
          onChange={(e, item) => setPage(item)}
        />
      </div>
      <div className={`${styles.navTitleCtnr} ms-Grid-col ms-lg4`}>
        <Label className={`${styles.navTitleLabel} ms-fontSize-28 ms-fontWeight-semibold`}>{state.currentPage.text}</Label>
      </div>
      <div className={`${styles.navMenuCtnr} ms-Grid-col ms-sm6 ms-md6 ms-lg4`}>
        <IconButton className={styles.navMenuIcon} iconProps={menuIcon} title="Menu" ariaLabel="Menu"></IconButton>
      </div>
    </div>
  );
};

export default Navigation;
