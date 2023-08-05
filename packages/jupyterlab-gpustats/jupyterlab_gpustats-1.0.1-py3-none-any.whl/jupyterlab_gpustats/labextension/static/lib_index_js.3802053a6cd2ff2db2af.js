(self["webpackChunkjupyterlab_gpustats"] = self["webpackChunkjupyterlab_gpustats"] || []).push([["lib_index_js"],{

/***/ "./lib/handler.js":
/*!************************!*\
  !*** ./lib/handler.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
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
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, 'jupyterlab-gpustats', endPoint);
    let response;
    try {
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, init, settings);
    }
    catch (error) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.NetworkError(error);
    }
    const data = await response.json();
    if (!response.ok) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.ResponseError(response, data.message);
    }
    return data;
}


/***/ }),

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
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/mainmenu */ "webpack/sharing/consume/default/@jupyterlab/mainmenu");
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");
/* harmony import */ var jupyterlab_topbar__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! jupyterlab-topbar */ "webpack/sharing/consume/default/jupyterlab-topbar/jupyterlab-topbar");
/* harmony import */ var jupyterlab_topbar__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(jupyterlab_topbar__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_3__);






/**
 * Initialization data for jupyterlab-gpustats server extension.
 */
const extension = {
    id: 'jupyterlab-gpustats',
    autoStart: true,
    requires: [jupyterlab_topbar__WEBPACK_IMPORTED_MODULE_2__.ITopBar, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ICommandPalette, _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_1__.IMainMenu, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.IThemeManager],
    activate: async (app, topBar) => {
        console.log('JupyterLab extension jupyterlab-gpustats is activated!');
        const gpuUtlWidget = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.Widget();
        const gpuMemWidget = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.Widget();
        const storageWidget = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.Widget();
        update();
        topBar.addItem('storage', storageWidget);
        topBar.addItem('gpu_mem', gpuMemWidget);
        topBar.addItem('gpu_utl', gpuUtlWidget);
        setInterval(update, 5000);
        function update() {
            (0,_handler__WEBPACK_IMPORTED_MODULE_4__.requestAPI)('metrics')
                .then(data => {
                gpuUtlWidget.node.textContent =
                    'GPU: ' + data['gpu']['utilization.gpu'] + '%';
                gpuMemWidget.node.textContent =
                    'GPU Mem: ' +
                        data['gpu']['memory.used'] +
                        ' of ' +
                        data['gpu']['memory.total'] +
                        'MB';
                storageWidget.node.textContent =
                    'Storage Used ' +
                        data['storage']['used'] +
                        ' / ' +
                        data['storage']['free'] + ' Free';
            })
                .catch(reason => {
                console.error(`The jupyterlab_gpustats_service_info server extension appears to be missing.\n${reason}`);
            });
        }
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (extension);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.3802053a6cd2ff2db2af.js.map