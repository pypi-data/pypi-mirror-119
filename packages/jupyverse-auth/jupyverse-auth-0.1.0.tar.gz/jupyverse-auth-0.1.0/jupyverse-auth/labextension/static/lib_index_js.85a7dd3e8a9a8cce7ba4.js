"use strict";
(self["webpackChunkjupyverse_auth"] = self["webpackChunkjupyverse_auth"] || []).push([["lib_index_js"],{

/***/ "./lib/components.js":
/*!***************************!*\
  !*** ./lib/components.js ***!
  \***************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "UserNameInput": () => (/* binding */ UserNameInput),
/* harmony export */   "UserIcon": () => (/* binding */ UserIcon),
/* harmony export */   "getUserIcon": () => (/* binding */ getUserIcon)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _style_img_user_svg__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../style/img/user.svg */ "./style/img/user.svg");




class UserNameInput extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ReactWidget {
    constructor(user, commands) {
        super();
        this._handleName = (event) => {
            this._name = event.target.value;
            this.update();
        };
        this._user = user;
        this._name = user.name;
        this._commands = commands;
    }
    getValue() {
        return this._name;
    }
    render() {
        const getButtons = () => {
            return this._user.logInMethods.map(id => {
                return (react__WEBPACK_IMPORTED_MODULE_2__.createElement("button", { id: "jp-Dialog-button", className: "jp-mod-reject jp-mod-styled", onClick: () => this._commands.execute(id) }, this._commands.label(id)));
            });
        };
        return (react__WEBPACK_IMPORTED_MODULE_2__.createElement("div", { className: "lm-Widget p-Widget jp-Dialog-body jp-Dialog-container" },
            react__WEBPACK_IMPORTED_MODULE_2__.createElement("label", null, "Who are you?"),
            react__WEBPACK_IMPORTED_MODULE_2__.createElement("input", { id: "jp-dialog-input-id", type: "text", className: "jp-Input-Dialog jp-mod-styled", value: this._name, onChange: this._handleName }),
            react__WEBPACK_IMPORTED_MODULE_2__.createElement("hr", null),
            getButtons()));
    }
}
class UserIcon extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ReactWidget {
    constructor(user) {
        super();
        this._profile = user;
        this._profile.ready.connect(() => this.update());
        this._profile.changed.connect(() => this.update());
    }
    render() {
        if (this._profile.isReady) {
            return (react__WEBPACK_IMPORTED_MODULE_2__.createElement("div", { className: "login-container" },
                getUserIcon(this._profile),
                react__WEBPACK_IMPORTED_MODULE_2__.createElement("span", { className: "login-username" }, this._profile.username)));
        }
        const avatar = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.LabIcon({
            name: 'userIcon',
            svgstr: _style_img_user_svg__WEBPACK_IMPORTED_MODULE_3__.default
        });
        return (react__WEBPACK_IMPORTED_MODULE_2__.createElement("div", { className: "login-container" },
            react__WEBPACK_IMPORTED_MODULE_2__.createElement("div", { className: "login-icon" },
                react__WEBPACK_IMPORTED_MODULE_2__.createElement(avatar.react, { className: "user-img", tag: "span", width: "28px", height: "28px" }))));
    }
}
const getUserIcon = (user) => {
    if (user.avatar) {
        return (react__WEBPACK_IMPORTED_MODULE_2__.createElement("div", { key: user.id, className: "login-icon" },
            react__WEBPACK_IMPORTED_MODULE_2__.createElement("img", { className: "user-img", src: user.avatar })));
    }
    if (!user.avatar) {
        return (react__WEBPACK_IMPORTED_MODULE_2__.createElement("div", { key: user.id, className: "login-icon", style: { backgroundColor: user.color } },
            react__WEBPACK_IMPORTED_MODULE_2__.createElement("span", null, user.initials)));
    }
};


/***/ }),

/***/ "./lib/docprovider.js":
/*!****************************!*\
  !*** ./lib/docprovider.js ***!
  \****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_docprovider__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/docprovider */ "webpack/sharing/consume/default/@jupyterlab/docprovider");
/* harmony import */ var _jupyterlab_docprovider__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docprovider__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_docprovider_lib_awareness__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/docprovider/lib/awareness */ "./node_modules/@jupyterlab/docprovider/lib/awareness.js");
/* harmony import */ var lib0_environment__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! lib0/environment */ "./node_modules/lib0/environment.js");
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./tokens */ "./lib/tokens.js");






/**
 * The default document provider plugin
 */
const docProviderPlugin = {
    id: 'jupyverse-auth:docprovider',
    requires: [_tokens__WEBPACK_IMPORTED_MODULE_3__.IUser],
    provides: _jupyterlab_docprovider__WEBPACK_IMPORTED_MODULE_0__.IDocumentProviderFactory,
    activate: (app, user) => {
        const server = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__.ServerConnection.makeSettings();
        const url = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.URLExt.join(server.wsUrl, 'api/yjs');
        const collaborative = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PageConfig.getOption('collaborative') === 'true' ? true : false;
        const factory = (options) => {
            const name = lib0_environment__WEBPACK_IMPORTED_MODULE_4__.getParam('--username', (0,_jupyterlab_docprovider_lib_awareness__WEBPACK_IMPORTED_MODULE_5__.getAnonymousUserName)());
            const color = '#' + lib0_environment__WEBPACK_IMPORTED_MODULE_4__.getParam('--usercolor', (0,_jupyterlab_docprovider_lib_awareness__WEBPACK_IMPORTED_MODULE_5__.getRandomColor)().slice(1));
            options.ymodel.awareness.setLocalStateField('user', {
                isAnonymous: user.isAnonymous,
                id: user.id,
                name: user.name || name,
                username: user.username,
                initials: user.initials,
                color: user.color || color,
                email: user.email,
                avatar: user.avatar
            });
            user.changed.connect(user => {
                options.ymodel.awareness.setLocalStateField('user', {
                    isAnonymous: user.isAnonymous,
                    id: user.id,
                    name: user.name || name,
                    username: user.username,
                    initials: user.initials,
                    color: user.color || color,
                    email: user.email,
                    avatar: user.avatar
                });
            });
            return collaborative
                ? new _jupyterlab_docprovider__WEBPACK_IMPORTED_MODULE_0__.WebSocketProviderWithLocks(Object.assign(Object.assign({}, options), { url }))
                : new _jupyterlab_docprovider__WEBPACK_IMPORTED_MODULE_0__.ProviderMock();
        };
        return factory;
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (docProviderPlugin);


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
/* harmony import */ var _user__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./user */ "./lib/user.js");
/* harmony import */ var _userMenu__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./userMenu */ "./lib/userMenu.js");
/* harmony import */ var _userPanel__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./userPanel */ "./lib/userPanel.js");
/* harmony import */ var _signInGitHub__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./signInGitHub */ "./lib/signInGitHub.js");
/* harmony import */ var _docprovider__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./docprovider */ "./lib/docprovider.js");
/* harmony import */ var _style_index_css__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../style/index.css */ "./style/index.css");






const plugins = [
    _user__WEBPACK_IMPORTED_MODULE_1__.default,
    _userMenu__WEBPACK_IMPORTED_MODULE_2__.default,
    _userPanel__WEBPACK_IMPORTED_MODULE_3__.default,
    _signInGitHub__WEBPACK_IMPORTED_MODULE_4__.default,
    _docprovider__WEBPACK_IMPORTED_MODULE_5__.default
];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);


/***/ }),

/***/ "./lib/signInGitHub.js":
/*!*****************************!*\
  !*** ./lib/signInGitHub.js ***!
  \*****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CommandIDs": () => (/* binding */ CommandIDs),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./tokens */ "./lib/tokens.js");
/* harmony import */ var _style_img_github_logo_svg__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../style/img/github-logo.svg */ "./style/img/github-logo.svg");






/**
 * A namespace for command IDs.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.github = 'jupyverse-auth:github';
})(CommandIDs || (CommandIDs = {}));
const plugin = {
    id: 'jupyverse-auth:github',
    autoStart: true,
    requires: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.IRouter, _tokens__WEBPACK_IMPORTED_MODULE_4__.IUser, _tokens__WEBPACK_IMPORTED_MODULE_4__.IUserMenu],
    activate: (app, router, user, menu) => {
        const { commands } = app;
        const icon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.LabIcon({
            name: 'githubIcon',
            svgstr: _style_img_github_logo_svg__WEBPACK_IMPORTED_MODULE_5__.default
        });
        commands.addCommand(CommandIDs.github, {
            label: 'Sign In with GitHub',
            icon: icon,
            isEnabled: () => user.isAnonymous,
            //isVisible: () => user.isAnonymous,
            execute: () => {
                const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
                const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.join(settings.baseUrl, '/auth/github/authorize?authentication_backend=cookie');
                const init = {
                    method: 'GET',
                    headers: { accept: 'application/json' }
                };
                _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, init, settings).then(async (resp) => {
                    const data = await resp.json();
                    window.location.href = data.authorization_url;
                });
            }
        });
        menu.insertItem(0, { command: CommandIDs.github });
        user.registerLogInMethod(CommandIDs.github);
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/tokens.js":
/*!***********************!*\
  !*** ./lib/tokens.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IUser": () => (/* binding */ IUser),
/* harmony export */   "IUserMenu": () => (/* binding */ IUserMenu),
/* harmony export */   "IUserPanel": () => (/* binding */ IUserPanel)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);

const IUser = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('jupyverse-auth:user');
const IUserMenu = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('jupyverse-auth:userMenu');
const IUserPanel = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('jupyverse-auth:userPanel');


/***/ }),

/***/ "./lib/user.js":
/*!*********************!*\
  !*** ./lib/user.js ***!
  \*********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CommandIDs": () => (/* binding */ CommandIDs),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__),
/* harmony export */   "User": () => (/* binding */ User)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_docprovider_lib_awareness__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @jupyterlab/docprovider/lib/awareness */ "./node_modules/@jupyterlab/docprovider/lib/awareness.js");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./tokens */ "./lib/tokens.js");
/* harmony import */ var _components__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./components */ "./lib/components.js");








/**
 * A namespace for command IDs.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.login = 'jupyverse-auth:login';
})(CommandIDs || (CommandIDs = {}));
const user = {
    id: 'jupyverse-auth:user',
    autoStart: true,
    requires: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.IRouter],
    provides: _tokens__WEBPACK_IMPORTED_MODULE_5__.IUser,
    activate: (app, router) => {
        const { commands } = app;
        const user = new User();
        commands.addCommand(CommandIDs.login, {
            execute: () => {
                if (!user.isReady) {
                    const body = new _components__WEBPACK_IMPORTED_MODULE_6__.UserNameInput(user, commands);
                    const dialog = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3__.Dialog({
                        title: 'Anonymous username',
                        body,
                        hasClose: false,
                        buttons: [
                            _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3__.Dialog.okButton({
                                label: 'Send'
                            })
                        ]
                    });
                    dialog.node.onclick = (event) => {
                        event.preventDefault();
                        event.stopImmediatePropagation();
                    };
                    dialog.launch().then(data => {
                        if (data.button.accept) {
                            const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__.ServerConnection.makeSettings();
                            const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.URLExt.join(settings.baseUrl, 'register');
                            const init = {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({
                                    email: data.value.replace(' ', '_') + '@foo.com',
                                    username: data.value,
                                    password: 'bar',
                                    name: data.value,
                                    color: user.color
                                })
                            };
                            _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__.ServerConnection.makeRequest(requestUrl, init, settings).then(async (resp) => {
                                const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__.ServerConnection.makeSettings();
                                const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.URLExt.join(settings.baseUrl, 'login');
                                const init = {
                                    method: 'POST',
                                    headers: {
                                        'Content-Type': 'application/x-www-form-urlencoded'
                                    },
                                    body: new URLSearchParams({
                                        username: data.value.replace(' ', '_') + '@foo.com',
                                        password: 'bar'
                                    })
                                };
                                _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__.ServerConnection.makeRequest(requestUrl, init, settings).then(async (resp) => {
                                    user.update();
                                });
                            });
                        }
                    });
                }
            }
        });
        router.register({
            pattern: /^\/lab/,
            command: CommandIDs.login
        });
        return user;
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (user);
class User {
    constructor() {
        this._isAnonymous = true;
        this._isReady = false;
        this._ready = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__.Signal(this);
        this._changed = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__.Signal(this);
        this._logInMethods = [];
        this._requestUser().then(() => {
            this._ready.emit(this._isReady);
        });
    }
    get id() {
        return this._id;
    }
    get name() {
        return this._name;
    }
    get username() {
        return this._username;
    }
    get initials() {
        return this._initials;
    }
    get color() {
        return this._color;
    }
    get email() {
        return this._email;
    }
    get avatar() {
        return this._avatar;
    }
    get isAnonymous() {
        return this._isAnonymous;
    }
    get isReady() {
        return this._isReady;
    }
    get ready() {
        return this._ready;
    }
    get changed() {
        return this._changed;
    }
    get logInMethods() {
        return this._logInMethods;
    }
    registerLogInMethod(command) {
        this._logInMethods.push(command);
    }
    update() {
        this._requestUser().then(() => {
            this._changed.emit();
        });
    }
    async _requestUser() {
        const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__.ServerConnection.makeSettings();
        const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.URLExt.join(settings.baseUrl, 'auth', 'users', 'me');
        return _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__.ServerConnection.makeRequest(requestUrl, {}, settings)
            .then(async (resp) => {
            if (!resp.ok) {
                this._isReady = false;
                this._isAnonymous = null;
                this._id = null;
                this._name = (0,_jupyterlab_docprovider_lib_awareness__WEBPACK_IMPORTED_MODULE_7__.getAnonymousUserName)();
                this._username = null;
                this._initials = null;
                this._color = null;
                this._email = null;
                this._avatar = null;
                return Promise.resolve();
            }
            const data = await resp.json();
            this._isReady = data.initialized;
            this._isAnonymous = data.anonymous;
            this._id = data.id;
            this._name = data.name || (0,_jupyterlab_docprovider_lib_awareness__WEBPACK_IMPORTED_MODULE_7__.getAnonymousUserName)();
            this._username = data.username || this._name;
            const name = this._name.split(' ');
            if (name.length > 0) {
                this._initials = name[0].substring(0, 1).toLocaleUpperCase();
            }
            if (name.length > 1) {
                this._initials += name[1].substring(0, 1).toLocaleUpperCase();
            }
            this._color = data.color || (0,_jupyterlab_docprovider_lib_awareness__WEBPACK_IMPORTED_MODULE_7__.getRandomColor)();
            this._email = data.email;
            this._avatar = data.avatar;
            return Promise.resolve();
        })
            .catch(err => console.error(err));
    }
}


/***/ }),

/***/ "./lib/userMenu.js":
/*!*************************!*\
  !*** ./lib/userMenu.js ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CommandIDs": () => (/* binding */ CommandIDs),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _components__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./components */ "./lib/components.js");
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./tokens */ "./lib/tokens.js");







/**
 * A namespace for command IDs.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.loggedInAs = 'jupyverse-auth:loggedInAs';
    CommandIDs.logout = 'jupyverse-auth:logout';
})(CommandIDs || (CommandIDs = {}));
const menu = {
    id: 'jupyverse-auth:userMenu',
    autoStart: true,
    requires: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.IRouter, _tokens__WEBPACK_IMPORTED_MODULE_5__.IUser],
    provides: _tokens__WEBPACK_IMPORTED_MODULE_5__.IUserMenu,
    activate: (app, router, user) => {
        const { shell, commands } = app;
        const spacer = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__.Widget();
        spacer.id = 'jp-topbar-spacer';
        spacer.addClass('topbar-spacer');
        shell.add(spacer, 'top', { rank: 1000 });
        const icon = new _components__WEBPACK_IMPORTED_MODULE_6__.UserIcon(user);
        icon.id = 'jp-UserIcon';
        // TODO: remove with next lumino release
        icon.node.onclick = (event) => {
            menu.open(window.innerWidth, 30);
        };
        const menu = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__.Menu({ commands });
        menu.id = 'jp-UserMenu-dropdown';
        menu.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.caretDownIcon;
        menu.title.className = 'jp-UserMenu-dropdown';
        menu.addItem({ type: 'separator' });
        commands.addCommand(CommandIDs.logout, {
            label: 'Sign Out',
            isEnabled: () => !user.isAnonymous,
            //isVisible: () => !user.isAnonymous,
            execute: () => {
                const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
                const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.join(settings.baseUrl, 'logout');
                const init = {
                    method: 'POST'
                };
                _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, init, settings).then(async (resp) => {
                    router.navigate('/', { hard: true });
                });
            }
        });
        menu.addItem({ command: CommandIDs.logout });
        const menuBar = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__.MenuBar();
        menuBar.id = 'jp-UserMenu';
        menuBar.node.insertBefore(icon.node, menuBar.node.firstChild);
        menuBar.addMenu(menu);
        // TODO: remove with next lumino release
        menuBar.node.onmousedown = (event) => {
            event.preventDefault();
            event.stopImmediatePropagation();
            menu.open(window.innerWidth, 30);
        };
        shell.add(menuBar, 'top', { rank: 1002 });
        return menu;
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (menu);


/***/ }),

/***/ "./lib/userPanel.js":
/*!**************************!*\
  !*** ./lib/userPanel.js ***!
  \**************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__),
/* harmony export */   "UserPanel": () => (/* binding */ UserPanel)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/fileeditor */ "webpack/sharing/consume/default/@jupyterlab/fileeditor");
/* harmony import */ var _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./tokens */ "./lib/tokens.js");
/* harmony import */ var _components__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./components */ "./lib/components.js");
/* harmony import */ var _style_img_user_svg__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../style/img/user.svg */ "./style/img/user.svg");










const userPanel = {
    id: 'jupyverse-auth:userPanel',
    requires: [_tokens__WEBPACK_IMPORTED_MODULE_7__.IUser, _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_4__.IEditorTracker, _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_5__.INotebookTracker],
    autoStart: true,
    provides: _tokens__WEBPACK_IMPORTED_MODULE_7__.IUserPanel,
    activate: (app, user, editor, notebook) => {
        const userPanel = new UserPanel(user);
        app.shell.add(userPanel, 'left', { rank: 300 });
        const collaboratorsChanged = (tracker) => {
            if (tracker.currentWidget === null) {
                userPanel.collaborators = [];
                return;
            }
            const model = tracker.currentWidget.context.model.sharedModel;
            const stateChanged = () => {
                //@ts-ignore
                const state = model.awareness.getStates();
                const collaborators = [];
                state.forEach((value, key) => {
                    const collaborator = {
                        isAnonymous: value.user.isAnonymous,
                        id: value.user.id,
                        name: value.user.name,
                        username: value.user.username,
                        initials: value.user.initials,
                        color: value.user.color,
                        email: value.user.email,
                        avatar: value.user.avatar
                    };
                    collaborators.push(collaborator);
                });
                userPanel.collaborators = collaborators;
            };
            //@ts-ignore
            model.awareness.on('change', stateChanged);
            stateChanged();
        };
        notebook.currentChanged.connect(collaboratorsChanged);
        editor.currentChanged.connect(collaboratorsChanged);
        return userPanel;
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (userPanel);
class UserPanel extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ReactWidget {
    constructor(user) {
        super();
        this.id = 'jp-user-panel';
        this.title.icon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
            name: 'userIcon',
            svgstr: _style_img_user_svg__WEBPACK_IMPORTED_MODULE_8__.default
        });
        this.addClass('jp-AuthWidget');
        this._profile = user;
        this._users = [];
        this._collaborators = [];
    }
    get collaborators() {
        return this._collaborators;
    }
    set collaborators(users) {
        this._collaborators = users;
        this.update();
    }
    onBeforeShow(msg) {
        super.onBeforeShow(msg);
        const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_3__.ServerConnection.makeSettings();
        const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.join(settings.baseUrl, 'auth', 'users');
        _jupyterlab_services__WEBPACK_IMPORTED_MODULE_3__.ServerConnection.makeRequest(requestUrl, {}, settings).then(async (resp) => {
            if (!resp.ok) {
                return;
            }
            const data = await resp.json();
            this._users = [];
            data.forEach((user) => {
                const name = user.name.split(' ');
                let initials = '';
                if (name.length > 0) {
                    initials += name[0].substring(0, 1).toLocaleUpperCase();
                }
                if (name.length > 1) {
                    initials += name[1].substring(0, 1).toLocaleUpperCase();
                }
                const collaborator = {
                    isAnonymous: true,
                    id: user.id,
                    name: user.name,
                    username: user.username || user.name,
                    initials,
                    color: user.color || '#E0E0E0',
                    email: null,
                    avatar: user.avatar
                };
                this._users.push(collaborator);
            });
            this.update();
        });
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_6__.createElement("div", { className: "jp-UserPanel" },
            react__WEBPACK_IMPORTED_MODULE_6__.createElement("div", { className: "panel-container" },
                (0,_components__WEBPACK_IMPORTED_MODULE_9__.getUserIcon)(this._profile),
                react__WEBPACK_IMPORTED_MODULE_6__.createElement("span", { className: "panel-username" }, this._profile.name)),
            react__WEBPACK_IMPORTED_MODULE_6__.createElement("h5", null, "Connected users"),
            react__WEBPACK_IMPORTED_MODULE_6__.createElement("hr", null),
            react__WEBPACK_IMPORTED_MODULE_6__.createElement("div", { className: "panel-container" }, this._users.map(user => {
                if (this._profile.id !== user.id) {
                    return (0,_components__WEBPACK_IMPORTED_MODULE_9__.getUserIcon)(user);
                }
            })),
            react__WEBPACK_IMPORTED_MODULE_6__.createElement("h5", null, "Collaborators"),
            react__WEBPACK_IMPORTED_MODULE_6__.createElement("hr", null),
            react__WEBPACK_IMPORTED_MODULE_6__.createElement("div", { className: "panel-container" }, this._collaborators.map(user => {
                if (this._profile.id !== user.id &&
                    this._profile.username !== user.username) {
                    return (0,_components__WEBPACK_IMPORTED_MODULE_9__.getUserIcon)(user);
                }
            }))));
    }
}


/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./style/index.css":
/*!***************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./style/index.css ***!
  \***************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/cssWithMappingToString.js */ "./node_modules/css-loader/dist/runtime/cssWithMappingToString.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
// Imports


var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, ".jp-AuthWidget {\n  padding: 10px;\n  color: var(--jp-ui-font-color1);\n  background: var(--jp-layout-color1);\n  font-size: 24px;\n  display: flex;\n  text-align: center;\n  justify-content: center;\n/*  align-items: center; */\n}\n\n#jp-topbar-spacer {\n  flex-grow: 1;\n  flex-shrink: 1;\n}\n\n#jp-UserIcon {\n  width: auto;\n  height: 33px;\n}\n\n#jp-UserMenu {\n  display: flex;\n  flex-direction: row;\n}\n\n.login-container {\n  height: 27px;\n  display: flex;\n  flex-direction: row;\n  text-align: center;\n  vertical-align: middle;\n}\n\n.login-container:hover {\n  cursor: pointer;\n}\n\n.login-icon {\n  margin: auto;\n  margin-top: 1px;\n  width: 25px;\n  height: 25px;\n  border-radius: 90px;\n  display: flex;\n  align-items: center;\n}\n\n.login-icon span {\n  margin: auto;\n  padding-top: 3px;\n  text-align: center;\n  vertical-align: middle;\n  fill: var(--jp-ui-font-color1);\n  color: var(--jp-ui-font-color1);\n}\n\n.user-img {\n  width: 25px;\n  height: 25px;\n  border-radius: 90px;\n  fill: var(--jp-ui-font-color1);\n  color: var(--jp-ui-font-color1);\n}\n\n.login-username {\n  margin: auto;\n  margin-left: 8px;\n  padding-top: 3px;\n  text-align: center;\n  vertical-align: middle;\n  color: var(--jp-ui-font-color1);\n}\n\n.jp-UserMenu-dropdown {\n  height: 30px;\n  padding: 4px;\n  padding-bottom: 0px;\n}\n\n.jp-github-icon {\n  margin-top: 4px;\n}\n\n.jp-Dialog-container {\n  min-height: 140;\n  overflow: hidden;\n}\n\n.jp-UserPanel span {\n  font-size: 12px;\n}\n\n.jp-UserPanel h5 {\n  margin-bottom: 0px;\n}\n\n.panel-container {\n  height: 27px;\n  display: flex;\n  flex-direction: row;\n  text-align: center;\n  vertical-align: middle;\n}\n\n.panel-username {\n  margin: auto;\n  margin-left: 8px;\n  padding-top: 3px;\n  text-align: center;\n  vertical-align: middle;\n  color: var(--jp-ui-font-color1);\n  font-size: 12px;\n}\n", "",{"version":3,"sources":["webpack://./style/index.css"],"names":[],"mappings":"AAAA;EACE,aAAa;EACb,+BAA+B;EAC/B,mCAAmC;EACnC,eAAe;EACf,aAAa;EACb,kBAAkB;EAClB,uBAAuB;AACzB,0BAA0B;AAC1B;;AAEA;EACE,YAAY;EACZ,cAAc;AAChB;;AAEA;EACE,WAAW;EACX,YAAY;AACd;;AAEA;EACE,aAAa;EACb,mBAAmB;AACrB;;AAEA;EACE,YAAY;EACZ,aAAa;EACb,mBAAmB;EACnB,kBAAkB;EAClB,sBAAsB;AACxB;;AAEA;EACE,eAAe;AACjB;;AAEA;EACE,YAAY;EACZ,eAAe;EACf,WAAW;EACX,YAAY;EACZ,mBAAmB;EACnB,aAAa;EACb,mBAAmB;AACrB;;AAEA;EACE,YAAY;EACZ,gBAAgB;EAChB,kBAAkB;EAClB,sBAAsB;EACtB,8BAA8B;EAC9B,+BAA+B;AACjC;;AAEA;EACE,WAAW;EACX,YAAY;EACZ,mBAAmB;EACnB,8BAA8B;EAC9B,+BAA+B;AACjC;;AAEA;EACE,YAAY;EACZ,gBAAgB;EAChB,gBAAgB;EAChB,kBAAkB;EAClB,sBAAsB;EACtB,+BAA+B;AACjC;;AAEA;EACE,YAAY;EACZ,YAAY;EACZ,mBAAmB;AACrB;;AAEA;EACE,eAAe;AACjB;;AAEA;EACE,eAAe;EACf,gBAAgB;AAClB;;AAEA;EACE,eAAe;AACjB;;AAEA;EACE,kBAAkB;AACpB;;AAEA;EACE,YAAY;EACZ,aAAa;EACb,mBAAmB;EACnB,kBAAkB;EAClB,sBAAsB;AACxB;;AAEA;EACE,YAAY;EACZ,gBAAgB;EAChB,gBAAgB;EAChB,kBAAkB;EAClB,sBAAsB;EACtB,+BAA+B;EAC/B,eAAe;AACjB","sourcesContent":[".jp-AuthWidget {\n  padding: 10px;\n  color: var(--jp-ui-font-color1);\n  background: var(--jp-layout-color1);\n  font-size: 24px;\n  display: flex;\n  text-align: center;\n  justify-content: center;\n/*  align-items: center; */\n}\n\n#jp-topbar-spacer {\n  flex-grow: 1;\n  flex-shrink: 1;\n}\n\n#jp-UserIcon {\n  width: auto;\n  height: 33px;\n}\n\n#jp-UserMenu {\n  display: flex;\n  flex-direction: row;\n}\n\n.login-container {\n  height: 27px;\n  display: flex;\n  flex-direction: row;\n  text-align: center;\n  vertical-align: middle;\n}\n\n.login-container:hover {\n  cursor: pointer;\n}\n\n.login-icon {\n  margin: auto;\n  margin-top: 1px;\n  width: 25px;\n  height: 25px;\n  border-radius: 90px;\n  display: flex;\n  align-items: center;\n}\n\n.login-icon span {\n  margin: auto;\n  padding-top: 3px;\n  text-align: center;\n  vertical-align: middle;\n  fill: var(--jp-ui-font-color1);\n  color: var(--jp-ui-font-color1);\n}\n\n.user-img {\n  width: 25px;\n  height: 25px;\n  border-radius: 90px;\n  fill: var(--jp-ui-font-color1);\n  color: var(--jp-ui-font-color1);\n}\n\n.login-username {\n  margin: auto;\n  margin-left: 8px;\n  padding-top: 3px;\n  text-align: center;\n  vertical-align: middle;\n  color: var(--jp-ui-font-color1);\n}\n\n.jp-UserMenu-dropdown {\n  height: 30px;\n  padding: 4px;\n  padding-bottom: 0px;\n}\n\n.jp-github-icon {\n  margin-top: 4px;\n}\n\n.jp-Dialog-container {\n  min-height: 140;\n  overflow: hidden;\n}\n\n.jp-UserPanel span {\n  font-size: 12px;\n}\n\n.jp-UserPanel h5 {\n  margin-bottom: 0px;\n}\n\n.panel-container {\n  height: 27px;\n  display: flex;\n  flex-direction: row;\n  text-align: center;\n  vertical-align: middle;\n}\n\n.panel-username {\n  margin: auto;\n  margin-left: 8px;\n  padding-top: 3px;\n  text-align: center;\n  vertical-align: middle;\n  color: var(--jp-ui-font-color1);\n  font-size: 12px;\n}\n"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./style/img/github-logo.svg":
/*!***********************************!*\
  !*** ./style/img/github-logo.svg ***!
  \***********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg width=\"16\" height=\"16\" viewBox=\"0 0 24 24\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\">\n<path d=\"M22.3903 6.12641C21.3172 4.24172 19.8617 2.74961 18.0232 1.64975C16.1845 0.549822 14.1772 0 11.9999 0C9.82282 0 7.81486 0.54999 5.97655 1.64975C4.13797 2.74956 2.68246 4.24172 1.60939 6.12641C0.536482 8.01104 0 10.0691 0 12.3005C0 14.9808 0.762885 17.3911 2.28904 19.5319C3.81503 21.6728 5.78638 23.1543 8.20293 23.9764C8.48422 24.0299 8.69245 23.9923 8.82785 23.8644C8.96329 23.7364 9.03093 23.5761 9.03093 23.3841C9.03093 23.3521 9.02825 23.0639 9.02305 22.5193C9.01769 21.9746 9.01517 21.4994 9.01517 21.094L8.65579 21.1577C8.42665 21.2008 8.13758 21.219 7.78859 21.2138C7.43977 21.2088 7.07764 21.1714 6.70271 21.1017C6.32762 21.0326 5.97874 20.8725 5.6558 20.6215C5.33302 20.3706 5.10388 20.0422 4.96844 19.6367L4.81219 19.2681C4.70805 19.0227 4.54409 18.7502 4.32009 18.4514C4.0961 18.1523 3.86959 17.9496 3.64045 17.8428L3.53105 17.7625C3.45816 17.7092 3.39051 17.6448 3.32796 17.5702C3.26546 17.4955 3.21867 17.4208 3.18742 17.346C3.15612 17.2711 3.18206 17.2096 3.26552 17.1614C3.34898 17.1133 3.4998 17.0899 3.71865 17.0899L4.03103 17.1377C4.23937 17.1805 4.49708 17.3084 4.80448 17.522C5.11171 17.7356 5.36427 18.0131 5.56222 18.3547C5.80192 18.7926 6.09071 19.1262 6.42941 19.3559C6.76784 19.5855 7.10906 19.7001 7.45274 19.7001C7.79642 19.7001 8.09325 19.6734 8.34335 19.6202C8.59318 19.5668 8.82757 19.4866 9.04642 19.3799C9.14017 18.6642 9.39541 18.1143 9.81193 17.73C9.21826 17.6661 8.68452 17.5697 8.21042 17.4417C7.7366 17.3134 7.24697 17.1053 6.74184 16.8167C6.23645 16.5285 5.81719 16.1707 5.48396 15.7438C5.15068 15.3166 4.87715 14.7559 4.66378 14.062C4.45029 13.3678 4.34352 12.5671 4.34352 11.6595C4.34352 10.3673 4.75506 9.26765 5.57798 8.35997C5.19249 7.38846 5.22888 6.29936 5.68727 5.0928C5.98936 4.99659 6.43735 5.06879 7.03102 5.30894C7.6248 5.54921 8.05954 5.75504 8.33569 5.92569C8.61184 6.09629 8.8331 6.24085 8.99979 6.3581C9.96872 6.08058 10.9686 5.94179 11.9998 5.94179C13.0309 5.94179 14.0311 6.08058 15 6.3581L15.5938 5.97388C15.9998 5.71751 16.4792 5.48257 17.031 5.269C17.5831 5.05555 18.0052 4.99675 18.297 5.09296C18.7656 6.29959 18.8074 7.38863 18.4217 8.36014C19.2446 9.26782 19.6563 10.3677 19.6563 11.6597C19.6563 12.5673 19.5492 13.3705 19.336 14.07C19.1226 14.7696 18.8467 15.3298 18.5083 15.7518C18.1695 16.1737 17.7475 16.5288 17.2424 16.8169C16.7372 17.1052 16.2474 17.3134 15.7735 17.4416C15.2995 17.5698 14.7658 17.6662 14.1721 17.7303C14.7136 18.2106 14.9843 18.9688 14.9843 20.0045V23.3837C14.9843 23.5756 15.0495 23.7359 15.1798 23.864C15.31 23.9918 15.5156 24.0295 15.7969 23.9759C18.2138 23.1539 20.1851 21.6724 21.7111 19.5314C23.2368 17.3907 24 14.9804 24 12.3C23.9995 10.0689 23.4627 8.01104 22.3903 6.12641Z\" fill=\"black\"/>\n</svg>\n");

/***/ }),

/***/ "./style/img/user.svg":
/*!****************************!*\
  !*** ./style/img/user.svg ***!
  \****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"16\" viewBox=\"-42 0 512 512\">\n\t<g class=\"jp-icon3 jp-icon-selectable\" fill=\"#616161\">\n    <path d=\"m210.351562 246.632812c33.882813 0 63.222657-12.152343 87.195313-36.128906 23.972656-23.972656 36.125-53.304687 36.125-87.191406 0-33.875-12.152344-63.210938-36.128906-87.191406-23.976563-23.96875-53.3125-36.121094-87.191407-36.121094-33.886718 0-63.21875 12.152344-87.191406 36.125s-36.128906 53.308594-36.128906 87.1875c0 33.886719 12.15625 63.222656 36.132812 87.195312 23.976563 23.96875 53.3125 36.125 87.1875 36.125zm0 0\"/>\n\t\t<path d=\"m426.128906 393.703125c-.691406-9.976563-2.089844-20.859375-4.148437-32.351563-2.078125-11.578124-4.753907-22.523437-7.957031-32.527343-3.308594-10.339844-7.808594-20.550781-13.371094-30.335938-5.773438-10.15625-12.554688-19-20.164063-26.277343-7.957031-7.613282-17.699219-13.734376-28.964843-18.199219-11.226563-4.441407-23.667969-6.691407-36.976563-6.691407-5.226563 0-10.28125 2.144532-20.042969 8.5-6.007812 3.917969-13.035156 8.449219-20.878906 13.460938-6.707031 4.273438-15.792969 8.277344-27.015625 11.902344-10.949219 3.542968-22.066406 5.339844-33.039063 5.339844-10.972656 0-22.085937-1.796876-33.046874-5.339844-11.210938-3.621094-20.296876-7.625-26.996094-11.898438-7.769532-4.964844-14.800782-9.496094-20.898438-13.46875-9.75-6.355468-14.808594-8.5-20.035156-8.5-13.3125 0-25.75 2.253906-36.972656 6.699219-11.257813 4.457031-21.003906 10.578125-28.96875 18.199219-7.605469 7.28125-14.390625 16.121094-20.15625 26.273437-5.558594 9.785157-10.058594 19.992188-13.371094 30.339844-3.199219 10.003906-5.875 20.945313-7.953125 32.523437-2.058594 11.476563-3.457031 22.363282-4.148437 32.363282-.679688 9.796875-1.023438 19.964844-1.023438 30.234375 0 26.726562 8.496094 48.363281 25.25 64.320312 16.546875 15.746094 38.441406 23.734375 65.066406 23.734375h246.53125c26.625 0 48.511719-7.984375 65.0625-23.734375 16.757813-15.945312 25.253906-37.585937 25.253906-64.324219-.003906-10.316406-.351562-20.492187-1.035156-30.242187zm0 0\"/>\n  </g>\n</svg>");

/***/ }),

/***/ "./style/index.css":
/*!*************************!*\
  !*** ./style/index.css ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./index.css */ "./node_modules/css-loader/dist/cjs.js!./style/index.css");

            

var options = {};

options.insert = "head";
options.singleton = false;

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_1__.default, options);



/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_1__.default.locals || {});

/***/ })

}]);
//# sourceMappingURL=lib_index_js.85a7dd3e8a9a8cce7ba4.js.map