(self["webpackChunk_retrolab_lab_extension"] = self["webpackChunk_retrolab_lab_extension"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/mainmenu */ "webpack/sharing/consume/default/@jupyterlab/mainmenu");
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _retrolab_application__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @retrolab/application */ "webpack/sharing/consume/default/@retrolab/application/@retrolab/application");
/* harmony import */ var _retrolab_application__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_retrolab_application__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _retrolab_ui_components__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @retrolab/ui-components */ "webpack/sharing/consume/default/@retrolab/ui-components/@retrolab/ui-components");
/* harmony import */ var _retrolab_ui_components__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_retrolab_ui_components__WEBPACK_IMPORTED_MODULE_8__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.









/**
 * The command IDs used by the application plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    /**
     * Launch RetroLab Tree
     */
    CommandIDs.launchRetroTree = 'retrolab:launch-tree';
    /**
     * Open RetroLab
     */
    CommandIDs.openRetro = 'retrolab:open-retro';
    /**
     * Open in Classic Notebook
     */
    CommandIDs.openClassic = 'retrolab:open-classic';
    /**
     * Open in JupyterLab
     */
    CommandIDs.openLab = 'retrolab:open-lab';
})(CommandIDs || (CommandIDs = {}));
/**
 * A plugin to add custom toolbar items to the notebook page
 */
const launchButtons = {
    id: '@retrolab/lab-extension:interface-switcher',
    autoStart: true,
    optional: [
        _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_4__.INotebookTracker,
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette,
        _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__.IMainMenu,
        _retrolab_application__WEBPACK_IMPORTED_MODULE_7__.IRetroShell,
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell
    ],
    activate: (app, notebookTracker, palette, menu, retroShell, labShell) => {
        if (!notebookTracker) {
            // to prevent showing the toolbar button in RetroLab
            return;
        }
        const { commands, shell } = app;
        const baseUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PageConfig.getBaseUrl();
        const isEnabled = () => {
            return (notebookTracker.currentWidget !== null &&
                notebookTracker.currentWidget === shell.currentWidget);
        };
        const addInterface = (option) => {
            const { command, icon, buttonLabel, commandLabel, urlPrefix } = option;
            commands.addCommand(command, {
                label: args => (args.noLabel ? '' : commandLabel),
                caption: commandLabel,
                icon,
                execute: () => {
                    const current = notebookTracker.currentWidget;
                    if (!current) {
                        return;
                    }
                    window.open(`${urlPrefix}${current.context.path}`);
                },
                isEnabled
            });
            if (palette) {
                palette.addItem({ command, category: 'Other' });
            }
            if (menu) {
                menu.viewMenu.addGroup([{ command }], 1);
            }
            notebookTracker.widgetAdded.connect(async (sender, panel) => {
                panel.toolbar.insertBefore('kernelName', buttonLabel, new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.CommandToolbarButton({
                    commands,
                    id: command,
                    args: { noLabel: 1 }
                }));
                await panel.context.ready;
                commands.notifyCommandChanged();
            });
        };
        // always add Classic
        addInterface({
            command: 'retrolab:open-classic',
            commandLabel: 'Open in Classic Notebook',
            buttonLabel: 'openClassic',
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_6__.jupyterIcon,
            urlPrefix: `${baseUrl}tree/`
        });
        if (!retroShell) {
            addInterface({
                command: 'retrolab:open-retro',
                commandLabel: 'Open in RetroLab',
                buttonLabel: 'openRetro',
                icon: _retrolab_ui_components__WEBPACK_IMPORTED_MODULE_8__.retroSunIcon,
                urlPrefix: `${baseUrl}retro/tree/`
            });
        }
        if (!labShell) {
            addInterface({
                command: 'retrolab:open-lab',
                commandLabel: 'Open in JupyterLab',
                buttonLabel: 'openLab',
                icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_6__.jupyterFaviconIcon,
                urlPrefix: `${baseUrl}doc/tree/`
            });
        }
    }
};
/**
 * A plugin to add a command to open the RetroLab Tree.
 */
const launchRetroTree = {
    id: '@retrolab/lab-extension:launch-retrotree',
    autoStart: true,
    requires: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5__.ITranslator],
    optional: [_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__.IMainMenu, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette],
    activate: (app, translator, menu, palette) => {
        const { commands } = app;
        const trans = translator.load('jupyterlab');
        const category = trans.__('Help');
        commands.addCommand(CommandIDs.launchRetroTree, {
            label: trans.__('Launch RetroLab File Browser'),
            execute: () => {
                window.open(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PageConfig.getBaseUrl() + 'retro/tree');
            }
        });
        if (menu) {
            const helpMenu = menu.helpMenu;
            helpMenu.addGroup([{ command: CommandIDs.launchRetroTree }], 1);
        }
        if (palette) {
            palette.addItem({ command: CommandIDs.launchRetroTree, category });
        }
    }
};
/**
 * Export the plugins as default.
 */
const plugins = [launchRetroTree, launchButtons];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.ef0ffc64b10eabf589e1.js.map