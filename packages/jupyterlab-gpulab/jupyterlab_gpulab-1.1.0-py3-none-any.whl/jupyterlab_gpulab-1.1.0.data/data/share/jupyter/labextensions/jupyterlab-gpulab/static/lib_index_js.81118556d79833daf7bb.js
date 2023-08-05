"use strict";
(self["webpackChunkjupyterlab_gpulab"] = self["webpackChunkjupyterlab_gpulab"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/mainmenu */ "webpack/sharing/consume/default/@jupyterlab/mainmenu");
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_2__);





/**
 * Initialization data for jupyterlab-gpulab server extension.
 */
const extension = {
    id: "jupyterlab-gpulab",
    autoStart: true,
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ICommandPalette, _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_1__.IMainMenu],
    activate: async (app, palette, mainMenu) => {
        document.title = "GPULab | JupyterLab Environment";
        const header = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Toolbar();
        header.id = 'gpulab-header';
        header.addClass('jp-gpulab-header');
        const logoWidget = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Widget();
        logoWidget.id = 'gpulab-logo';
        logoWidget.addClass('jp-gpulab-logo');
        header.addItem("logo", logoWidget);
        header.addItem("spacer", _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Toolbar.createSpacerItem());
        app.shell.add(header, 'header', undefined);
        const { commands } = app;
        const portal_command = 'gpulab:launch_portal';
        const blog_command = 'gpulab:launch_blog';
        const faq_command = 'gpulab:launch_faq';
        const contact_command = 'gpulab:launch_contact';
        const twitter_command = 'gpulab:twitter';
        const github_command = 'gpulab:github';
        commands.addCommand(portal_command, {
            label: 'GPULab Account Portal',
            caption: 'Open the GPULab portal.',
            execute: (args) => {
                window.open(`https://portal.gpulab.io`, 'gpulab-external');
            }
        });
        commands.addCommand(blog_command, {
            label: 'GPULab Blog',
            caption: 'Open the GPULab blog/',
            execute: (args) => {
                window.open(`https://gpulab.io/blog/`, 'gpulab-external');
            }
        });
        commands.addCommand(faq_command, {
            label: 'GPULab FAQ',
            caption: 'Open the GPULab FAQ page.',
            execute: (args) => {
                window.open(`https://gpulab.io/faq/`, 'gpulab-external');
            }
        });
        commands.addCommand(contact_command, {
            label: 'GPULab Contact',
            caption: 'Open the GPULab contact page.',
            execute: (args) => {
                window.open(`https://gpulab.io/blog/`, 'gpulab-external');
            }
        });
        commands.addCommand(twitter_command, {
            label: 'GPULab Twitter',
            caption: 'Follow GPULab on Twitter.',
            execute: (args) => {
                window.open(`https://twitter.com/gpulabio`, 'gpulab-external');
            }
        });
        commands.addCommand(github_command, {
            label: 'GPULab GitHub',
            caption: 'GPULab GitHub repository.',
            execute: (args) => {
                window.open(`https://github.com/gpulab`, 'gpulab-external');
            }
        });
        const category = 'GPULab';
        palette.addItem({ command: portal_command, category: category, args: {} });
        palette.addItem({ command: blog_command, category: category, args: {} });
        palette.addItem({ command: faq_command, category: category, args: {} });
        palette.addItem({ command: contact_command, category: category, args: {} });
        // Create a GPULab Menu
        const gpuLabMenu = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Menu({ commands });
        gpuLabMenu.title.label = 'GPULab';
        mainMenu.addMenu(gpuLabMenu, { rank: 1000 });
        gpuLabMenu.addItem({ command: portal_command, args: {} });
        gpuLabMenu.addItem({ command: blog_command, args: {} });
        gpuLabMenu.addItem({ command: faq_command, args: {} });
        gpuLabMenu.addItem({ command: contact_command, args: {} });
        gpuLabMenu.addItem({ command: twitter_command, args: {} });
        gpuLabMenu.addItem({ command: github_command, args: {} });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (extension);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.81118556d79833daf7bb.js.map