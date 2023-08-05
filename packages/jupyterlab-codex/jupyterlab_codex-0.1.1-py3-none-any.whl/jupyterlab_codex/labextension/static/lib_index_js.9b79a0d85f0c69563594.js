"use strict";
(self["webpackChunkjupyterlab_codex"] = self["webpackChunkjupyterlab_codex"] || []).push([["lib_index_js"],{

/***/ "./lib/codex.js":
/*!**********************!*\
  !*** ./lib/codex.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "getCodeCells": () => (/* binding */ getCodeCells),
/* harmony export */   "getCodeCellTextAsPrompt": () => (/* binding */ getCodeCellTextAsPrompt),
/* harmony export */   "generateCodeInCell": () => (/* binding */ generateCodeInCell)
/* harmony export */ });
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");

function getCodeCells(notebook) {
    const codeCells = [];
    notebook.widgets.forEach((cell) => {
        if (cell.model.type === 'code' && notebook.isSelectedOrActive(cell)) {
            codeCells.push(cell);
        }
    });
    return codeCells;
}
function getCodeCellTextAsPrompt(codeCells) {
    return codeCells.map((cell) => cell.model.value.text).join('\n');
}
async function generateCodeInCell(codeCell, prompt, config) {
    try {
        if (!config) {
            throw new Error('Codex config is not defined');
        }
        const payload = Object.assign({}, config, {
            prompt,
        });
        console.log(payload);
        const data = await (0,_handler__WEBPACK_IMPORTED_MODULE_0__.requestAPI)('completion', {
            method: 'POST',
            body: JSON.stringify(payload),
        });
        console.log(data);
        if (data.choices && data.choices.length > 0) {
            const texts = data.choices[0].text.split('\n');
            for (const text of texts) {
                codeCell.model.value.text += text;
                codeCell.model.value.text += '\n';
                // sleep displayLineTimeout ms
                await new Promise(resolve => setTimeout(resolve, config.displayLineTimeout));
            }
        }
    }
    catch (error) {
        console.error(`The jupyterlab_codex server extension appears to be missing.\n${error}`);
    }
}


/***/ }),

/***/ "./lib/handler.js":
/*!************************!*\
  !*** ./lib/handler.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "requestAPI": () => (/* binding */ requestAPI)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);


/**
 * Call the API extension
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
async function requestAPI(endPoint = '', init = {}) {
    // Make request to Jupyter API
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, 'jupyterlab-codex', // API Namespace
    endPoint);
    let response;
    try {
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, init, settings);
    }
    catch (error) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.NetworkError(error);
    }
    let data = await response.text();
    if (data.length > 0) {
        try {
            data = JSON.parse(data);
        }
        catch (error) {
            console.log('Not a JSON response body.', response);
        }
    }
    if (!response.ok) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.ResponseError(response, data.message || data);
    }
    return data;
}


/***/ }),

/***/ "./lib/icon.js":
/*!*********************!*\
  !*** ./lib/icon.js ***!
  \*********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CODEX_ICON": () => (/* binding */ CODEX_ICON)
/* harmony export */ });
const CODEX_ICON = '<svg viewBox="0 0 320 364" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><linearGradient id="a" gradientUnits="userSpaceOnUse" x1="131.52" x2="188.48" y1="70.77" y2="169.42"><stop offset="0" stop-color="#b6facf"></stop><stop offset=".12" stop-color="#bfe5ff"></stop><stop offset=".28" stop-color="#d6d6ff"></stop><stop offset=".48" stop-color="#ffc5f4"></stop><stop offset=".65" stop-color="#ffdcbd"></stop><stop offset=".83" stop-color="#d7f5ae"></stop><stop offset="1" stop-color="#b6facf"></stop></linearGradient><linearGradient id="b" x1="118.15" x2="201.86" xlink:href="#a" y1="109.49" y2="254.49"></linearGradient><linearGradient id="c" x1="131.52" x2="188.48" xlink:href="#a" y1="194.58" y2="293.23"></linearGradient><path d="m309.44 83.52-138.88-80.18a21.13 21.13 0 0 0 -21.12 0l-138.88 80.18a21.15 21.15 0 0 0 -10.56 18.3v160.36a21.15 21.15 0 0 0 10.56 18.3l138.88 80.18a21.13 21.13 0 0 0 21.12 0l138.88-80.18a21.15 21.15 0 0 0 10.56-18.3v-160.36a21.15 21.15 0 0 0 -10.56-18.3z" fill="#0f0f1c"></path><path d="m54.48 123 95.6-55.19c5.38-3.11 14.46-3.11 19.84 0l95.6 55.19a3.41 3.41 0 0 0 1.68.45 3.36 3.36 0 0 0 1.68-6.27l-95.59-55.18c-7.45-4.3-19.13-4.3-26.58 0l-95.59 55.2a3.36 3.36 0 1 0 3.36 5.8z" fill="url(#a)"></path><path d="m270.54 150.73a1.65 1.65 0 0 0 -.06-.32c0-.1 0-.21-.07-.31a.91.91 0 0 0 -.11-.3 3.09 3.09 0 0 0 -.14-.32l-.05-.11-.11-.15c-.07-.1-.13-.2-.21-.3l-.22-.23-.24-.23-.29-.2-.16-.12-95.59-55.14c-7.45-4.3-19.13-4.3-26.58 0l-95.59 55.19a3.36 3.36 0 1 0 3.36 5.81l95.6-55.19c5.38-3.1 14.46-3.1 19.84 0l90.56 52.28-20.08 11.61-67.11-38.8c-7.45-4.3-19.13-4.3-26.58 0l-95.59 55.19a3.36 3.36 0 0 0 1.68 6.27 3.31 3.31 0 0 0 1.68-.45l95.6-55.19c5.38-3.11 14.46-3.11 19.84 0l63.76 36.81-20.08 11.59-40.31-23.28c-7.45-4.3-19.13-4.3-26.58 0l-95.59 55.16a.91.91 0 0 0 -.16.11 1.94 1.94 0 0 0 -.29.21l-.24.22-.22.24-.21.29c0 .05-.08.1-.11.16v.1a3.09 3.09 0 0 0 -.14.32c0 .1-.08.2-.11.3s0 .21-.07.31a1.91 1.91 0 0 0 -.06.33v.64a1.65 1.65 0 0 0 .06.32c0 .1 0 .21.07.31a.91.91 0 0 0 .11.3 3.09 3.09 0 0 0 .14.32v.11a.55.55 0 0 1 .08.1 2.69 2.69 0 0 0 .39.5l.14.16a4 4 0 0 0 .62.47l95.56 55.18a29 29 0 0 0 26.58 0l95.59-55.19a3.36 3.36 0 0 0 -3.36-5.82l-95.6 55.19c-5.38 3.1-14.46 3.1-19.84 0l-90.53-52.18 20.08-11.6 67.11 38.75a29 29 0 0 0 26.58 0l95.59-55.15a3.36 3.36 0 0 0 -3.36-5.82l-95.6 55.19c-5.38 3.11-14.46 3.11-19.84 0l-63.76-36.85 20.08-11.59 40.31 23.28a29 29 0 0 0 26.58 0l95.56-55.21a3.16 3.16 0 0 0 .62-.47 1 1 0 0 0 .14-.15 2.69 2.69 0 0 0 .39-.5.79.79 0 0 0 .08-.11l.05-.1a3.09 3.09 0 0 0 .14-.32c0-.1.08-.2.11-.3s.05-.21.07-.31a1.91 1.91 0 0 0 .06-.33v-.32c0-.11 0-.25 0-.36zm-100.62 52.6c-5.38 3.11-14.46 3.11-19.84 0l-37-21.33 37-21.33c5.38-3.11 14.46-3.11 19.84 0l37 21.33z" fill="url(#b)"></path><path d="m265.52 241-95.6 55.19c-5.38 3.11-14.46 3.11-19.84 0l-95.6-55.19a3.36 3.36 0 1 0 -3.36 5.82l95.59 55.18a29 29 0 0 0 26.58 0l95.59-55.2a3.36 3.36 0 0 0 -3.36-5.82z" fill="url(#c)"></path></svg>';


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _toolbar__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./toolbar */ "./lib/toolbar.js");


/**
 * Initialization data for the jupyterlab-codex extension.
 */
const plugin = {
    id: 'jupyterlab-codex:plugin',
    autoStart: true,
    optional: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__.ISettingRegistry],
    activate: async (app, settingRegistry) => {
        try {
            console.log('JupyterLab extension jupyterlab-codex is activated!');
            if (!settingRegistry) {
                throw new Error('No setting registry');
            }
            app.docRegistry.addWidgetExtension('Notebook', new _toolbar__WEBPACK_IMPORTED_MODULE_1__.CodexButtonExtension(plugin.id, settingRegistry));
        }
        catch (err) {
            console.error('Failed to load settings for jupyterlab-codex.', err);
        }
    },
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/toolbar.js":
/*!************************!*\
  !*** ./lib/toolbar.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CodexButtonExtension": () => (/* binding */ CodexButtonExtension)
/* harmony export */ });
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/disposable */ "webpack/sharing/consume/default/@lumino/disposable");
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_disposable__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _icon__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./icon */ "./lib/icon.js");
/* harmony import */ var _codex__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./codex */ "./lib/codex.js");





class CodexButtonExtension {
    constructor(pluginId, settingRegistry) {
        this.pluginId = pluginId;
        this.settingRegistry = settingRegistry;
        this.settingRegistry.load(this.pluginId).then(settings => {
            settings.changed.connect(this.updateConfig.bind(this));
            this.updateConfig(settings);
        });
    }
    createNew(widget, context) {
        const button = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ToolbarButton({
            tooltip: 'Codex It!',
            icon: new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.LabIcon({
                name: 'codex',
                svgstr: _icon__WEBPACK_IMPORTED_MODULE_3__.CODEX_ICON,
            }),
            onClick: async () => {
                const codeCells = (0,_codex__WEBPACK_IMPORTED_MODULE_4__.getCodeCells)(widget.content);
                const prompt = (0,_codex__WEBPACK_IMPORTED_MODULE_4__.getCodeCellTextAsPrompt)(codeCells);
                if (codeCells.length < 1) {
                    return;
                }
                //get last code cell
                const lastCodeCell = codeCells[codeCells.length - 1];
                return (0,_codex__WEBPACK_IMPORTED_MODULE_4__.generateCodeInCell)(lastCodeCell, prompt, this.config);
            },
        });
        widget.toolbar.insertAfter('cellType', 'codex', button);
        return new _lumino_disposable__WEBPACK_IMPORTED_MODULE_0__.DisposableDelegate(() => {
            button.dispose();
        });
    }
    updateConfig(settings) {
        this.config = settings.composite;
    }
}


/***/ })

}]);
//# sourceMappingURL=lib_index_js.9b79a0d85f0c69563594.js.map