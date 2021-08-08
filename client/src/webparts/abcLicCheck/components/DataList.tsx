import * as React from "react";
import { Page, Report, Header, IItem } from "./IAbcLicCheckState";
import { TextField } from "@fluentui/react/lib/TextField";
import { Toggle } from "@fluentui/react/lib/Toggle";
import { Announced } from "@fluentui/react/lib/Announced";
import {
  DetailsList,
  DetailsListLayoutMode,
  Selection,
  SelectionMode,
  IColumn,
  IDetailsColumnRenderTooltipProps,
  IDetailsHeaderProps,
  IDetailsListStyles,
  IViewport,
} from "@fluentui/react/lib/DetailsList";
import { MarqueeSelection } from "@fluentui/react/lib/MarqueeSelection";
import {
  Dropdown,
  IDropdownOption,
  IIconProps,
  IconButton,
  ThemeProvider,
  ScrollablePane,
} from "office-ui-fabric-react";
import { TooltipHost } from "@fluentui/react/lib/Tooltip";
import { IRenderFunction } from "@fluentui/react/lib/Utilities";
import styles from "./styles/DetailsList.module.scss";
import { StylesProvider } from "@material-ui/styles";
import { useState } from "react";

export interface DetailsListState {
  columns: Object;
  filteredColumns: IColumn[];
  items: IItem[];
  selectionDetails: string;
  isModalSelection: boolean;
  isCompactMode: boolean;
  isToday: boolean;
  showControl: boolean;
  colFilters: Array<Header>;
  selectedFilters: Object;
  announcedMessage?: string;
  report: Report;
  height: number;
}

export class DataList extends React.Component<
  { report: Report },
  DetailsListState
> {
  private _selection: Selection;
  private _allItems: IItem[];
  private _headers: Array<Header>;

  constructor(props: { report: Report }) {
    super(props);

    this._allItems = this.props.report.data;
    this._headers = this.props.report.headers;

    this._updateWindowDimensions = this._updateWindowDimensions.bind(this);

    const columns: Object = {
      created: {
        key: "created",
        name: "Created",
        fieldName: "created",
        data: "date",
        ariaLabel: "Column operations for Created, Press to sort on Created",
        isResizable: true,
        isRowHeader: true,
        minWidth: 80,
        maxWidth: 120,
        isSorted: true,
        isSortedDescending: true,
        sortAscendingAriaLabel: "Sorted Older to Newer",
        sortDescendingLabel: "Sorted Newer to Older",
        onColumnClick: this._onColumnClick,
        isPadded: true,
        onRender: (item: IItem) => {
          let newDate = new Date(String(item.created));
          return (
            <span>{`${
              newDate.getMonth() + 1
            }/${newDate.getDate()}/${newDate.getFullYear()}`}</span>
          );
        },
      },
      report_type: {
        key: "report_type",
        name: "Report Type",
        fieldName: "report_type",
        data: "string",
        ariaLabel:
          "Column operations for Report Type, Press to sort on Report Type",
        isResizable: true,
        isRowHeader: true,
        minWidth: 100,
        maxWidth: 260,
        isSorted: true,
        isSortedDescending: false,
        sortAscendingAriaLabel: "Sorted A to Z",
        sortDescendingLabel: "Sorted Z to A",
        onColumnClick: this._onColumnClick,
        isPadded: true,
      },
      lic_num: {
        key: "lic_num",
        name: "License Number",
        fieldName: "lic_num",
        data: "number",
        ariaLabel:
          "Column operations for License Number, Press to sort on License Number",
        isResizable: true,
        isRowHeader: true,
        minWidth: 100,
        maxWidth: 260,
        isSorted: true,
        isSortedDescending: false,
        sortAscendingAriaLabel: "Sorted Lowest to Highest",
        sortDescendingLabel: "Sorted Highest to Lowest",
        onColumnClick: this._onColumnClick,
        isPadded: true,
      },
      status_from: {
        key: "status_from",
        name: "Status From",
        fieldName: "status_from",
        data: "string",
        ariaLabel:
          "Column operations for Status From, Press to sort on Status From",
        isResizable: true,
        isRowHeader: true,
        minWidth: 60,
        maxWidth: 100,
        isSorted: true,
        isSortedDescending: false,
        sortAscendingAriaLabel: "Sorted A to Z",
        sortDescendingLabel: "Sorted Z to A",
        onColumnClick: this._onColumnClick,
        isPadded: true,
      },
      status_to: {
        key: "status_to",
        name: "Status To",
        fieldName: "status_to",
        data: "string",
        ariaLabel:
          "Column operations for Status To, Press to sort on Status To",
        isResizable: true,
        isRowHeader: true,
        minWidth: 60,
        maxWidth: 100,
        isSorted: true,
        isSortedDescending: false,
        sortAscendingAriaLabel: "Sorted A to Z",
        sortDescendingLabel: "Sorted Z to A",
        onColumnClick: this._onColumnClick,
        isPadded: true,
      },
      status: {
        key: "status",
        name: "Status",
        fieldName: "status",
        data: "string",
        ariaLabel: "Column operations for Status, Press to sort on Status",
        isResizable: true,
        isRowHeader: true,
        minWidth: 80,
        maxWidth: 120,
        isSorted: true,
        isSortedDescending: false,
        sortAscendingAriaLabel: "Sorted A to Z",
        sortDescendingLabel: "Sorted Z to A",
        onColumnClick: this._onColumnClick,
        isPadded: true,
      },
      lic_type: {
        key: "lic_type",
        name: "License Type",
        fieldName: "lic_type",
        data: "string",
        ariaLabel:
          "Column operations for License Type, Press to sort on License Type",
        isResizable: true,
        isRowHeader: true,
        minWidth: 60,
        maxWidth: 100,
        isSorted: true,
        isSortedDescending: false,
        sortAscendingAriaLabel: "Sorted A to Z",
        sortDescendingLabel: "Sorted Z to A",
        onColumnClick: this._onColumnClick,
        isPadded: true,
      },
      lic_dup: {
        key: "lic_dup",
        name: "License Dup.",
        fieldName: "lic_dup",
        data: "string",
        ariaLabel:
          "Column operations for License Dup., Press to sort on License Dup.",
        isResizable: true,
        isRowHeader: true,
        minWidth: 60,
        maxWidth: 100,
        isSorted: true,
        isSortedDescending: false,
        sortAscendingAriaLabel: "Sorted A to Z",
        sortDescendingLabel: "Sorted Z to A",
        onColumnClick: this._onColumnClick,
        isPadded: true,
      },
      issue_date: {
        key: "issue_date",
        name: "Issue Date",
        fieldName: "issue_date",
        data: "date",
        ariaLabel:
          "Column operations for Issue Date, Press to sort on Issue Date",
        isResizable: true,
        isRowHeader: true,
        minWidth: 80,
        maxWidth: 120,
        isSorted: true,
        isSortedDescending: false,
        sortAscendingAriaLabel: "Sorted Older to Newer",
        sortDescendingLabel: "Sorted Newer to Older",
        onColumnClick: this._onColumnClick,
        isPadded: true,
        onRender: (item: IItem) => {
          if (item.issue_date) {
            let newDate = new Date(String(item.issue_date));
            return (
              <span>{`${
                newDate.getMonth() + 1
              }/${newDate.getDate()}/${newDate.getFullYear()}`}</span>
            );
          }
        },
      },
      exp_date: {
        key: "exp_date",
        name: "Expiration Date",
        fieldName: "exp_date",
        data: "date",
        ariaLabel:
          "Column operations for Expiration Date, Press to sort on Expiration Date",
        isResizable: true,
        isRowHeader: true,
        minWidth: 80,
        maxWidth: 120,
        isSorted: true,
        isSortedDescending: false,
        sortAscendingAriaLabel: "Sorted Older to Newer",
        sortDescendingLabel: "Sorted Newer to Older",
        onColumnClick: this._onColumnClick,
        isPadded: true,
        onRender: (item: IItem) => {
          if (item.exp_date) {
            let newDate = new Date(String(item.exp_date));
            return (
              <span>{`${
                newDate.getMonth() + 1
              }/${newDate.getDate()}/${newDate.getFullYear()}`}</span>
            );
          }
        },
      },
      acct_name: {
        key: "acct_name",
        name: "Account Name",
        fieldName: "acct_name",
        data: "string",
        ariaLabel:
          "Column operations for Account Name, Press to sort on Account Name",
        isResizable: true,
        isRowHeader: true,
        minWidth: 180,
        maxWidth: 360,
        isSorted: true,
        isSortedDescending: false,
        sortAscendingAriaLabel: "Sorted A to Z",
        sortDescendingLabel: "Sorted Z to A",
        onColumnClick: this._onColumnClick,
        isPadded: true,
      },
      acct_own: {
        key: "acct_own",
        name: "Account Owner",
        fieldName: "acct_own",
        data: "string",
        ariaLabel:
          "Column operations for Account Owner, Press to sort on Account Owner",
        isResizable: true,
        isRowHeader: true,
        minWidth: 180,
        maxWidth: 360,
        isSorted: true,
        isSortedDescending: false,
        sortAscendingAriaLabel: "Sorted A to Z",
        sortDescendingLabel: "Sorted Z to A",
        onColumnClick: this._onColumnClick,
        isPadded: true,
      },
      acct_street: {
        key: "acct_street",
        name: "Account Street",
        fieldName: "acct_street",
        data: "string",
        ariaLabel:
          "Column operations for Account Street, Press to sort on Account Street",
        isResizable: true,
        isRowHeader: true,
        minWidth: 180,
        maxWidth: 360,
        isSorted: true,
        isSortedDescending: false,
        sortAscendingAriaLabel: "Sorted A to Z",
        sortDescendingLabel: "Sorted Z to A",
        onColumnClick: this._onColumnClick,
        isPadded: true,
      },
      acct_city: {
        key: "acct_city",
        name: "Account City",
        fieldName: "acct_city",
        data: "string",
        ariaLabel:
          "Column operations for Account City, Press to sort on Account City",
        isResizable: true,
        isRowHeader: true,
        minWidth: 160,
        maxWidth: 320,
        isSorted: true,
        isSortedDescending: false,
        sortAscendingAriaLabel: "Sorted A to Z",
        sortDescendingLabel: "Sorted Z to A",
        onColumnClick: this._onColumnClick,
        isPadded: true,
      },
      acct_state: {
        key: "acct_state",
        name: "Account State",
        fieldName: "acct_state",
        data: "string",
        ariaLabel:
          "Column operations for Account State, Press to sort on Account State",
        isResizable: true,
        isRowHeader: true,
        minWidth: 80,
        maxWidth: 120,
        isSorted: true,
        isSortedDescending: false,
        sortAscendingAriaLabel: "Sorted A to Z",
        sortDescendingLabel: "Sorted Z to A",
        onColumnClick: this._onColumnClick,
        isPadded: true,
      },
      acct_zip: {
        key: "acct_zip",
        name: "Account Zip",
        fieldName: "acct_zip",
        data: "string",
        ariaLabel:
          "Column operations for Account Zip, Press to sort on Account Zip",
        isResizable: true,
        isRowHeader: true,
        minWidth: 80,
        maxWidth: 120,
        isSorted: true,
        isSortedDescending: false,
        sortAscendingAriaLabel: "Sorted A to Z",
        sortDescendingLabel: "Sorted Z to A",
        onColumnClick: this._onColumnClick,
        isPadded: true,
      },
      mail_street: {
        key: "mail_street",
        name: "Mail Street",
        fieldName: "mail_street",
        data: "string",
        ariaLabel:
          "Column operations for Mail Street, Press to sort on Mail Street",
        isResizable: true,
        isRowHeader: true,
        minWidth: 180,
        maxWidth: 360,
        isSorted: true,
        isSortedDescending: false,
        sortAscendingAriaLabel: "Sorted A to Z",
        sortDescendingLabel: "Sorted Z to A",
        onColumnClick: this._onColumnClick,
        isPadded: true,
      },
      mail_city: {
        key: "mail_city",
        name: "Mail City",
        fieldName: "mail_city",
        data: "string",
        ariaLabel:
          "Column operations for Mail City, Press to sort on Mail City",
        isResizable: true,
        isRowHeader: true,
        minWidth: 160,
        maxWidth: 360,
        isSorted: true,
        isSortedDescending: false,
        sortAscendingAriaLabel: "Sorted A to Z",
        sortDescendingLabel: "Sorted Z to A",
        onColumnClick: this._onColumnClick,
        isPadded: true,
      },
      mail_state: {
        key: "mail_state",
        name: "Mail State",
        fieldName: "mail_state",
        data: "string",
        ariaLabel:
          "Column operations for Mail State, Press to sort on Mail State",
        isResizable: true,
        isRowHeader: true,
        minWidth: 80,
        maxWidth: 120,
        isSorted: true,
        isSortedDescending: false,
        sortAscendingAriaLabel: "Sorted A to Z",
        sortDescendingLabel: "Sorted Z to A",
        onColumnClick: this._onColumnClick,
        isPadded: true,
      },
      mail_zip: {
        key: "mail_zip",
        name: "Mail Zip",
        fieldName: "mail_zip",
        data: "string",
        ariaLabel: "Column operations for Mail Zip, Press to sort on Mail Zip",
        isResizable: true,
        isRowHeader: true,
        minWidth: 80,
        maxWidth: 120,
        isSorted: true,
        isSortedDescending: false,
        sortAscendingAriaLabel: "Sorted A to Z",
        sortDescendingLabel: "Sorted Z to A",
        onColumnClick: this._onColumnClick,
        isPadded: true,
      },
      action: {
        key: "action",
        name: "Action",
        fieldName: "action",
        data: "string",
        ariaLabel: "Column operations for Action, Press to sort on Action",
        isResizable: true,
        isRowHeader: true,
        minWidth: 80,
        maxWidth: 120,
        isSorted: true,
        isSortedDescending: false,
        sortAscendingAriaLabel: "Sorted A to Z",
        sortDescendingLabel: "Sorted Z to A",
        onColumnClick: this._onColumnClick,
        isPadded: true,
      },
      conditions: {
        key: "conditions",
        name: "Conditions",
        fieldName: "conditions",
        data: "string",
        ariaLabel:
          "Column operations for Conditions, Press to sort on Conditions",
        isResizable: true,
        isRowHeader: true,
        minWidth: 80,
        maxWidth: 120,
        isSorted: true,
        isSortedDescending: false,
        sortAscendingAriaLabel: "Sorted A to Z",
        sortDescendingLabel: "Sorted Z to A",
        onColumnClick: this._onColumnClick,
        isPadded: true,
      },
      escrow: {
        key: "escrow",
        name: "Escrow",
        fieldName: "escrow",
        data: "string",
        ariaLabel: "Column operations for Escrow, Press to sort on Escrow",
        isResizable: true,
        isRowHeader: true,
        minWidth: 180,
        maxWidth: 360,
        isSorted: true,
        isSortedDescending: false,
        sortAscendingAriaLabel: "Sorted A to Z",
        sortDescendingLabel: "Sorted Z to A",
        onColumnClick: this._onColumnClick,
        isPadded: true,
      },
      district: {
        key: "district",
        name: "District",
        fieldName: "district",
        data: "string",
        ariaLabel: "Column operations for District, Press to sort on District",
        isResizable: true,
        isRowHeader: true,
        minWidth: 60,
        maxWidth: 100,
        isSorted: true,
        isSortedDescending: false,
        sortAscendingAriaLabel: "Sorted A to Z",
        sortDescendingLabel: "Sorted Z to A",
        onColumnClick: this._onColumnClick,
        isPadded: true,
      },
      trans_from: {
        key: "trans_from",
        name: "Trans. From",
        fieldName: "trans_from",
        data: "string",
        ariaLabel:
          "Column operations for Trans From, Press to sort on Trans From",
        isResizable: true,
        isRowHeader: true,
        minWidth: 80,
        maxWidth: 120,
        isSorted: true,
        isSortedDescending: false,
        sortAscendingAriaLabel: "Sorted A to Z",
        sortDescendingLabel: "Sorted Z to A",
        onColumnClick: this._onColumnClick,
        isPadded: true,
      },
      trans_to: {
        key: "trans_to",
        name: "Trans. To",
        fieldName: "trans_to",
        data: "string",
        ariaLabel: "Column operations for Trans To, Press to sort on Trans To",
        isResizable: true,
        isRowHeader: true,
        minWidth: 80,
        maxWidth: 120,
        isSorted: true,
        isSortedDescending: false,
        sortAscendingAriaLabel: "Sorted A to Z",
        sortDescendingLabel: "Sorted Z to A",
        onColumnClick: this._onColumnClick,
        isPadded: true,
      },
      geocode: {
        key: "geocode",
        name: "Geocode",
        fieldName: "geocode",
        data: "number",
        ariaLabel: "Column operations for Geocode, Press to sort on Geocode",
        isResizable: true,
        isRowHeader: true,
        minWidth: 60,
        maxWidth: 100,
        isSorted: true,
        isSortedDescending: false,
        sortAscendingAriaLabel: "Sorted Lowest to Highest",
        sortDescendingLabel: "Sorted Highest to Lowest",
        onColumnClick: this._onColumnClick,
        isPadded: true,
      },
    };

    const filteredColumns = this._filterColumns(columns, this._headers);

    const colFilters = this._headers.filter((e) => {
      if (e.filter) return e;
    });

    const selectedFilters = {
      filter1: { dropdown: colFilters[0], textField: "" },
      filter2: { dropdown: colFilters[1], textField: "" },
      filter3: { dropdown: colFilters[2], textField: "" },
    };

    this._selection = new Selection({
      onSelectionChanged: () => {
        this.setState({
          selectionDetails: this._getSelectionDetails(),
        });
      },
    });

    this.state = {
      items: this._allItems,
      columns: columns,
      filteredColumns: filteredColumns,
      selectionDetails: this._getSelectionDetails(),
      isModalSelection: false,
      isCompactMode: false,
      isToday: true,
      showControl: false,
      colFilters: colFilters,
      selectedFilters: selectedFilters,
      announcedMessage: undefined,
      report: this.props.report,
      height: 0,
    };
  }

  public render() {
    const {
      columns,
      filteredColumns,
      isCompactMode,
      items,
      selectionDetails,
      isModalSelection,
      isToday,
      showControl,
      colFilters,
      selectedFilters,
      announcedMessage,
    } = this.state;
    const filterIcon: IIconProps = { iconName: "FilterSettings" };
    const controlHeight = 200;

    const gridStyles: Partial<IDetailsListStyles> = {
      root: {
        height: "100%",
        overflowX: "scroll",
        selectors: {
          "& [role=grid]": {
            display: "flex",
            flexDirection: "column",
            alignItems: "start",
            height: "100%",
          },
        },
      },
      headerWrapper: {
        flex: "0 0 auto",
      },
      // TODO Create function to fix height modifier based on breakpoints
      contentWrapper: {
        flex: "1 1 auto",
        overflowY: "auto",
        overflowX: "hidden",
        height: showControl
          ? this.state.height * 0.6 - controlHeight
          : this.state.height * 0.6,
      },
    };

    return (
      <ThemeProvider>
        {showControl && (
          <div
            style={{ height: controlHeight }}
            className={`${styles.controlWrapper} ${
              showControl ? "ms-slideDownIn20" : "ms-slideDownOut"
            } ms-Grid`}
          >
            <div className={`${styles.controlRow} ms-Grid-row`}>
              <div className={`ms-Grid-col ms-sm4 ms-md4 ms-lg-2`}>
                <Toggle
                  label="Enable compact mode"
                  checked={isCompactMode}
                  onChange={this._onChangeCompactMode}
                  onText="Compact"
                  offText="Normal"
                  className={styles.control}
                />
              </div>
              <div className={`ms-Grid-col ms-sm4 ms-md4 ms-lg-2`}>
                <Toggle
                  label="Enable modal selection"
                  checked={isModalSelection}
                  onChange={this._onChangeModalSelection}
                  onText="Modal"
                  offText="Normal"
                  className={styles.control}
                />
              </div>
              <div className={`ms-Grid-col ms-sm4 ms-md4 ms-lg-8`}>
                <Toggle
                  label="Change report range"
                  checked={isToday}
                  onChange={this._onChangeViewToday}
                  onText="Today"
                  offText="All"
                  className={styles.control}
                />
              </div>
            </div>
            <div className={`${styles.controlRow} ms-Grid-row`}>
              <div className={`ms-Grid-col ms-md4 ms-lg-8`}>
                <Dropdown
                  className={styles.control}
                  label="Filter by"
                  placeholder="Select column..."
                  selectedKey={selectedFilters["filter1"].dropdown.key}
                  options={colFilters}
                  onChange={(e, item) => this._onSelectFilter("filter1", item)}
                />
                <TextField
                  onChange={(ev, text) =>
                    this._onChangeText(ev, text, "filter1")
                  }
                  value={selectedFilters["filter1"].textField}
                  className={styles.control}
                />
                <Announced
                  message={`Number of items after filter applied: ${items.length}.`}
                />
              </div>
              <div className={`ms-Grid-col ms-md4 ms-lg-8`}>
                <Dropdown
                  className={styles.control}
                  label="Filter by"
                  placeholder="Select column..."
                  selectedKey={selectedFilters["filter2"].dropdown.key}
                  options={colFilters}
                  onChange={(e, item) => this._onSelectFilter("filter2", item)}
                />
                <TextField
                  onChange={(ev, text) =>
                    this._onChangeText(ev, text, "filter2")
                  }
                  className={styles.control}
                />
                <Announced
                  message={`Number of items after filter applied: ${items.length}.`}
                />
              </div>
              <div className={`ms-Grid-col ms-md4 ms-lg-8`}>
                <Dropdown
                  className={styles.control}
                  label="Filter by"
                  placeholder="Select column..."
                  selectedKey={selectedFilters["filter3"].dropdown.key}
                  options={colFilters}
                  onChange={(e, item) => this._onSelectFilter("filter3", item)}
                />
                <TextField
                  onChange={(ev, text) =>
                    this._onChangeText(ev, text, "filter3")
                  }
                  className={styles.control}
                />
                <Announced
                  message={`Number of items after filter applied: ${items.length}.`}
                />
              </div>
            </div>
          </div>
        )}
        <div className={styles.selectionDetails}>{selectionDetails}</div>
        <Announced message={selectionDetails} />
        {announcedMessage ? (
          <Announced message={announcedMessage} />
        ) : undefined}
        <div className={`ms-Grid-row`} dir="rtl">
          <div className={`ms-Grid-col ms-sm12`}>
            <IconButton
              className={styles.filterIcon}
              iconProps={filterIcon}
              onClick={this._onClickFilter}
              title="Filter"
              ariaLabel="Filter"
            ></IconButton>
          </div>
        </div>
        <div className={`ms-Grid-row`}>
          <div className={`${styles.detailsList} ms-Grid-col ms-sm12`}>
            {isModalSelection ? (
              <MarqueeSelection selection={this._selection}>
                <DetailsList
                  items={items}
                  compact={isCompactMode}
                  columns={filteredColumns}
                  selectionMode={SelectionMode.multiple}
                  getKey={this._getId}
                  setKey="multiple"
                  layoutMode={DetailsListLayoutMode.justified}
                  isHeaderVisible={true}
                  selection={this._selection}
                  selectionPreservedOnEmptyClick={true}
                  onItemInvoked={this._onItemInvoked}
                  enterModalSelectionOnTouch={true}
                  ariaLabelForSelectionColumn="Toggle selection"
                  ariaLabelForSelectAllCheckbox="Toggle selection for all items"
                  checkButtonAriaLabel="Row checkbox"
                />
              </MarqueeSelection>
            ) : (
              <DetailsList
                items={items}
                compact={isCompactMode}
                columns={filteredColumns}
                selectionMode={SelectionMode.none}
                getKey={this._getId}
                setKey="none"
                styles={gridStyles}
                layoutMode={DetailsListLayoutMode.justified}
                isHeaderVisible={true}
                onItemInvoked={this._onItemInvoked}
                onRenderDetailsHeader={this.onRenderDetailsHeader}
              />
            )}
          </div>
        </div>
      </ThemeProvider>
    );
  }

  public componentDidMount() {
    this._updateWindowDimensions();
    window.addEventListener("resize", this._updateWindowDimensions);
  }

  public componentDidUpdate(
    previousProps: any,
    previousState: DetailsListState
  ) {
    // Handle Modal Selection
    if (
      previousState.isModalSelection !== this.state.isModalSelection &&
      !this.state.isModalSelection
    ) {
      this._selection.setAllSelected(false);
    }
  }

  public componentWillUnmount() {
    window.removeEventListener("resize", this._updateWindowDimensions);
  }

  private _updateWindowDimensions() {
    this.setState({ height: window.innerHeight });
  }

  private _getId(item: any, index?: number): string {
    return item.id;
  }

  private _onChangeCompactMode = (
    ev: React.MouseEvent<HTMLElement>,
    checked: boolean
  ): void => {
    this.setState({ isCompactMode: checked });
  };

  private _onClickFilter = (): void => {
    this.setState({ showControl: !this.state.showControl });
  };

  private _onChangeModalSelection = (
    ev: React.MouseEvent<HTMLElement>,
    checked: boolean
  ): void => {
    this.setState({ isModalSelection: checked });
  };

  private _onChangeViewToday = (
    ev: React.MouseEvent<HTMLElement>,
    checked: boolean
  ): void => {
    this.setState({ isToday: checked });
  };

  private _onChangeText = (
    ev: React.FormEvent<HTMLInputElement | HTMLTextAreaElement>,
    text: string,
    currFilter: string
  ): void => {
    let selected = this.state.selectedFilters;

    selected[currFilter].textField = text;
    this.setState({ selectedFilters: selected });

    const filtText1 = selected["filter1"].textField.toLowerCase();
    const filtText2 = selected["filter2"].textField.toLowerCase();
    const filtText3 = selected["filter3"].textField.toLowerCase();

    const allItemsCopy = this._allItems.filter((i) => {
      return (
        i[selected["filter1"].dropdown.key]
          .toString()
          .toLowerCase()
          .indexOf(filtText1) > -1 &&
        i[selected["filter2"].dropdown.key]
          .toString()
          .toLowerCase()
          .indexOf(filtText2) > -1 &&
        i[selected["filter3"].dropdown.key]
          .toString()
          .toLowerCase()
          .indexOf(filtText3) > -1
      );
    });

    this.setState({
      items:
        selected["filter1"].textField ||
        selected["filter2"].textField ||
        selected["filter3"].textField
          ? allItemsCopy
          : this._allItems,
    });
  };

  private _onItemInvoked(item: any): void {
    alert(`Item invoked: ${item.name}`);
  }

  private _getSelectionDetails(): string {
    const selectionCount = this._selection.getSelectedCount();

    switch (selectionCount) {
      case 0:
        return "No items selected";
      case 1:
        return (
          "1 item selected: " +
          (this._selection.getSelection()[0] as IItem).lic_num
        );
      default:
        return `${selectionCount} items selected`;
    }
  }

  private _onColumnClick = (
    ev: React.MouseEvent<HTMLElement>,
    column: IColumn
  ): void => {
    const { filteredColumns, items } = this.state;
    const newColumns: IColumn[] = filteredColumns.slice();
    const currColumn: IColumn = newColumns.filter(
      (currCol) => column.key === currCol.key
    )[0];
    newColumns.forEach((newCol: IColumn) => {
      if (newCol === currColumn) {
        currColumn.isSortedDescending = !currColumn.isSortedDescending;
        currColumn.isSorted = true;
        this.setState({
          announcedMessage: `${currColumn.name} is sorted ${
            currColumn.isSortedDescending ? "descending" : "ascending"
          }`,
        });
      } else {
        newCol.isSorted = false;
        newCol.isSortedDescending = true;
      }
    });
    const newItems = _copyAndSort(
      items,
      currColumn.fieldName!,
      currColumn.isSortedDescending
    );
    this.setState({
      columns: newColumns,
      items: newItems,
    });
  };

  private _filterColumns(columns: Object, headers: Array<Header>): IColumn[] {
    let filtered: IColumn[] = [];
    headers.map((header) => {
      let key = header.key;
      filtered.push(columns[key]);
    });
    return filtered;
  }

  private _onSelectFilter = (filterNum: string, colFilter: any): void => {
    let selectedFiltersCopy = this.state.selectedFilters;
    selectedFiltersCopy[filterNum].dropdown = colFilter;

    this.setState({ selectedFilters: selectedFiltersCopy });
  };

  private onRenderDetailsHeader: IRenderFunction<IDetailsHeaderProps> = (
    props,
    defaultRender
  ) => {
    if (!props) {
      return null;
    }
    const onRenderColumnHeaderTooltip: IRenderFunction<IDetailsColumnRenderTooltipProps> =
      (tooltipHostProps) => <TooltipHost {...tooltipHostProps} />;
    return defaultRender!({
      ...props,
      onRenderColumnHeaderTooltip,
    });
  };
}

function _copyAndSort<T>(
  items: T[],
  columnKey: string,
  isSortedDescending?: boolean
): T[] {
  const key = columnKey as keyof T;
  return items
    .slice(0)
    .sort((a: T, b: T) =>
      (isSortedDescending ? a[key] < b[key] : a[key] > b[key]) ? 1 : -1
    );
}
