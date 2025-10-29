======= 📁 react-spa/ =======
📄 Description:
postcss.config.js
    📕 Stats: LOC 6 | funcs 0 | classes 0 | exports 0
release.sh
    📕 Imports: shebang:/bin/bash
    📕 Stats: LOC 37 | funcs 0 | classes 0 | exports 0
    📕 Doc: Run the npm build script
tailwind.config.js
    📕 Stats: LOC 41 | funcs 0 | classes 0 | exports 0
=== 📁 _Project_Documentation/ ===
📄 Description:
=== 📁 lib/ ===
📄 Description:
=== 📁 public/ ===
📄 Description:
=== 📁 src/ ===
📄 Description:
App.test.tsx
    📕 Imports: react, @testing-library/react, ./App
    📕 Stats: LOC 9 | funcs 0 | classes 0 | exports 0
⭐️ App.tsx
    📕 Imports: @reactour/tour, react, react-router-dom, ./components/LoadingScreen, ./features/breadcrumbs/types, ./features/changeManual/components/ContainerChangeManual, ./features/changeManual/effects, ./features/files/components/ContainerFileModal, ./features/header/components/MobileHeader, ./features/search/components/modalSearch/ContainerSearchWindow, ./features/sidenav/effects, ./features/systemInfo/components/ContainerSystemModal, ./pages/Dcc, ./pages/Documents, ./pages/FAQ, ./pages/Home, ./pages/Id, ./pages/Kks, ./pages/Search, ./utils/appContext, ./utils/dataContext
    📕 Functions: App, createSelectableManuals
    📕 Stats: LOC 217 | funcs 2 | classes 0 | exports 0
index.css
    📕 Stats: LOC 90 | funcs 0 | classes 0 | exports 0
    📕 Doc: selectors:15 media_queries:0
⭐️ index.tsx
    📕 Imports: react, react-dom/client, ./index.css, ./App, ./reportWebVitals
    📕 Stats: LOC 17 | funcs 0 | classes 0 | exports 0
react-app-env.d.ts
    📕 Stats: LOC 1 | funcs 0 | classes 0 | exports 0
reportWebVitals.ts
    📕 Imports: web-vitals
    📕 Functions: reportWebVitals
    📕 Stats: LOC 15 | funcs 1 | classes 0 | exports 0
setupTests.ts
    📕 Imports: @testing-library/jest-dom
    📕 Stats: LOC 5 | funcs 0 | classes 0 | exports 0
types.ts
    📕 Stats: LOC 3 | funcs 0 | classes 0 | exports 0
📁 src/components/
    📄 Description:
    Button.tsx
        📕 Functions: Button, clicked
        📕 Exports: Button
        📕 Stats: LOC 88 | funcs 2 | classes 0 | exports 1
    Checkmark.tsx
        📕 Imports: react, ../../src/icons/checkmark.svg
        📕 Functions: CheckMark, toggle
        📕 Exports: CheckMark
        📕 Stats: LOC 51 | funcs 2 | classes 0 | exports 1
    Footer.tsx
        📕 Functions: Footer
        📕 Exports: Footer
        📕 Stats: LOC 19 | funcs 1 | classes 0 | exports 1
    LoadingScreen.tsx
        📕 Imports: react, ../utils/appContext
        📕 Functions: LoadingScreen
        📕 Exports: LoadingScreen
        📕 Stats: LOC 16 | funcs 1 | classes 0 | exports 1
    Page.tsx
        📕 Imports: react, ../features/breadcrumbs/components/breadcrumbs, ../features/header/components/Header, ../features/sidenav/components/SideNav, ./Footer
        📕 Functions: Page
        📕 Exports: Page
        📕 Stats: LOC 32 | funcs 1 | classes 0 | exports 1
    Spinner.tsx
        📕 Imports: react, ../icons/loading.svg, ../icons/loading_dark.svg, ../utils/appContext
        📕 Functions: Spinner
        📕 Exports: Spinner
        📕 Stats: LOC 29 | funcs 1 | classes 0 | exports 1
📁 src/features/
    📄 Description:
    📁 src/features/breadcrumbs/
        📄 Description:
        types.ts
            📕 Stats: LOC 5 | funcs 0 | classes 0 | exports 0
        useBreadcrumbs.ts
            📕 Imports: react, ../../utils/dataContext, ../../utils/translations, ./types
            📕 Functions: useBreadcrumbs, createBreadCrumbs, findBreadcrumbs, createStaticBreadcrumb
            📕 Exports: useBreadcrumbs
            📕 Stats: LOC 93 | funcs 4 | classes 0 | exports 1
        📁 src/features/breadcrumbs/components/
            📄 Description:
            breadcrumbs.tsx
                📕 Imports: react, react-router-dom, ../../../utils/dataContext, ../types
                📕 Functions: Breadcrumbs, createBreadcrumbs, handleClick
                📕 Exports: Breadcrumbs
                📕 Stats: LOC 59 | funcs 3 | classes 0 | exports 1
    📁 src/features/changeManual/
        📄 Description:
        effects.ts
            📕 Imports: axios, ../../utils/api
            📕 Exports: getManuals
            📕 Stats: LOC 7 | funcs 0 | classes 0 | exports 1
        📁 src/features/changeManual/components/
            📄 Description:
            ChangeManualModal.tsx
                📕 Imports: react, react-router-dom, ../../../utils/appContext, ../../../utils/dataContext, ../../../utils/translations, ../../../icons/close_dark.svg
                📕 Functions: ChangeManualModal, changeManual
                📕 Exports: ChangeManualModal
                📕 Stats: LOC 57 | funcs 2 | classes 0 | exports 1
            ContainerChangeManual.tsx
                📕 Imports: react, ../../../utils/appContext, ./ChangeManualModal
                📕 Functions: ContainerChangeManual
                📕 Exports: ContainerChangeManual
                📕 Stats: LOC 23 | funcs 1 | classes 0 | exports 1
    📁 src/features/dashboard/
        📄 Description:
        📁 src/features/dashboard/components/
            📄 Description:
            Dashboard.tsx
                📕 Imports: react, ../../../utils/translations
                📕 Functions: Dashboard
                📕 Exports: Dashboard
                📕 Stats: LOC 23 | funcs 1 | classes 0 | exports 1
            DashboardSearch.tsx
                📕 Imports: react, ../../../icons/search.svg, ../../../utils/translations, react-router-dom, ../../../helpers/Search
                📕 Functions: DashboardSearch
                📕 Exports: DashboardSearch
                📕 Stats: LOC 48 | funcs 1 | classes 0 | exports 1
            ProjectTitle.tsx
                📕 Imports: react, ../../../utils/dataContext, ../../../utils/translations
                📕 Functions: ProjectTitle
                📕 Exports: ProjectTitle
                📕 Stats: LOC 34 | funcs 1 | classes 0 | exports 1
    📁 src/features/dccKksSearch/
        📄 Description:
        📁 src/features/dccKksSearch/components/
            📄 Description:
            DccKksSearch.tsx
                📕 Imports: react, react-router-dom, ../../../utils/dataContext, ../../../utils/translations, ../../../utils/useClickOutsideBounds
                📕 Functions: DccKksSearch, flatten, handleChange, findDcc, findKks, renderSearch
                📕 Exports: DccKksSearch
                📕 Stats: LOC 169 | funcs 6 | classes 0 | exports 1
    📁 src/features/files/
        📄 Description:
        📁 src/features/files/components/
            📄 Description:
            ContainerFileModal.tsx
                📕 Imports: react, ../../../utils/appContext, ./FileModal
                📕 Functions: ContainerSearchWindow
                📕 Exports: ContainerSearchWindow
                📕 Stats: LOC 23 | funcs 1 | classes 0 | exports 1
            FileModal.tsx
                📕 Imports: react, ../../../utils/appContext, ../../../utils/translations, ../../../icons/close_dark.svg
                📕 Functions: FileModal, getFileType, renderFile
                📕 Exports: FileModal
                📕 Stats: LOC 75 | funcs 3 | classes 0 | exports 1
    📁 src/features/header/
        📄 Description:
        📁 src/features/header/components/
            📄 Description:
            Header.tsx
                📕 Imports: ../../../components/Button, ./LanguageSelect, ../../../images/logo_dark.svg, ../../../utils/translations, ../../../utils/dataContext, react, react-router-dom, ../../../utils/appContext, ../../tour/components/AppTour, ../../../icons/info_light.svg, ../../../icons/help_light.svg, react-helmet
                📕 Functions: Header, renderChangeManual
                📕 Exports: Header
                📕 Stats: LOC 114 | funcs 2 | classes 0 | exports 1
            LanguageSelect.tsx
                📕 Imports: react, ../../../utils/appContext, ../../../utils/translations, ../../../utils/useClickOutsideBounds
                📕 Functions: LanguageSelect, click, Flag, renderLanguages
                📕 Exports: LanguageSelect
                📕 Stats: LOC 71 | funcs 4 | classes 0 | exports 1
            MobileHeader.tsx
                📕 Imports: react, ../../dccKksSearch/components/DccKksSearch, ../../sidenav/components/Structure, ../../../images/logo_dark.svg, ../../../icons/search.svg, ../../../icons/close.svg, ../../../icons/hamburger.svg, react-router-dom, ./LanguageSelect, ../../../utils/dataContext, ../../../utils/appContext, ../../../components/Button, ../../../utils/translations, ../../../icons/info.svg, ../../../icons/help_light.svg, react-helmet, ../../dashboard/components/DashboardSearch
                📕 Functions: MobileHeader, Expanded
                📕 Exports: MobileHeader
                📕 Stats: LOC 143 | funcs 2 | classes 0 | exports 1
    📁 src/features/search/
        📄 Description:
        effects.ts
            📕 Imports: axios, ../../utils/api
            📕 Exports: QuerySearch
            📕 Stats: LOC 20 | funcs 0 | classes 0 | exports 1
        📁 src/features/search/components/
            📄 Description:
            SearchInput.tsx
                📕 Imports: react, ../../../icons/search.svg, ../effects, ../../../utils/dataContext, ../../../utils/translations, ../../../utils/appContext, ../../../helpers/Search
                📕 Functions: SearchInput, createCategorizedResult
                📕 Exports: SearchInput
                📕 Stats: LOC 128 | funcs 2 | classes 0 | exports 1
            SearchWindow.tsx
                📕 Imports: react, ../../table/components/Table, ./SearchInput
                📕 Functions: SearchWindow
                📕 Exports: SearchWindow
                📕 Stats: LOC 22 | funcs 1 | classes 0 | exports 1
            📁 src/features/search/components/modalSearch/
                📄 Description:
                ContainerSearchWindow.tsx
                    📕 Imports: react, ../../../../utils/appContext, ./ModalSearchWindow
                    📕 Functions: ContainerSearchWindow
                    📕 Exports: ContainerSearchWindow
                    📕 Stats: LOC 23 | funcs 1 | classes 0 | exports 1
                ModalSearchInput.tsx
                    📕 Imports: react, ../../../../icons/search.svg, ../../effects, ../../../../utils/translations, ../../../../utils/appContext, ../../../../helpers/Search, react-router-dom, ../../../../components/Button
                    📕 Functions: ModalSearchInput, viewAsTable
                    📕 Exports: ModalSearchInput
                    📕 Stats: LOC 123 | funcs 2 | classes 0 | exports 1
                ModalSearchWindow.tsx
                    📕 Imports: react, ../../../../icons/folder.svg, ../../../../components/Button, react-router-dom, ../../../../utils/appContext, ./ModalSearchInput, ../../../../utils/translations
                    📕 Functions: ModalSearchWindow, createData, categorizeData, showMore, getCategoryFilteredData, renderCategories, renderCategorizedData
                    📕 Exports: ModalSearchWindow
                    📕 Stats: LOC 150 | funcs 7 | classes 0 | exports 1
    📁 src/features/sidenav/
        📄 Description:
        effects.ts
            📕 Imports: axios, ../../utils/api
            📕 Exports: getInitialStructure, getAllParts, getAllDocuments, getAllDesigns, getTableOfContents
            📕 Stats: LOC 36 | funcs 0 | classes 0 | exports 5
        📁 src/features/sidenav/components/
            📄 Description:
            SideNav.tsx
                📕 Imports: ./Structure, ../../../icons/arrow_double_right.svg, ../../../icons/arrow_double_left.svg, ../../../images/logo.svg, ../../dccKksSearch/components/DccKksSearch, react-router-dom, react, ../../../utils/dataContext, ../../../utils/translations, ../../dashboard/components/DashboardSearch
                📕 Functions: SideNav, SideNavCollapsed, SideNavOpen
                📕 Exports: SideNav
                📕 Stats: LOC 73 | funcs 3 | classes 0 | exports 1
            Structure.tsx
                📕 Imports: react, react-router-dom, ../../../utils/dataContext, ../../../utils/translations
                📕 Functions: Structure, toggleMenuItem, collapseChildren, expandChildren, expandChildrenM3Project, scrollToElement
                📕 Exports: Structure
                📕 Stats: LOC 213 | funcs 6 | classes 0 | exports 1
    📁 src/features/systemInfo/
        📄 Description:
        📁 src/features/systemInfo/components/
            📄 Description:
            ContainerSystemModal.tsx
                📕 Imports: react, ../../../utils/appContext, ./SystemInfoModal
                📕 Functions: ContainerSystemInfoModal
                📕 Exports: ContainerSystemInfoModal
                📕 Stats: LOC 23 | funcs 1 | classes 0 | exports 1
            SystemInfoModal.tsx
                📕 Imports: react, ../../../utils/appContext, ../../../utils/dataContext, ../../../utils/translations, ../../../icons/close_dark.svg
                📕 Functions: SystemInfoModal, Column, getManualLanguages
                📕 Exports: SystemInfoModal
                📕 Stats: LOC 167 | funcs 3 | classes 0 | exports 1
    📁 src/features/table/
        📄 Description:
        CreateColumns.tsx
            📕 Imports: @tanstack/react-table, ../../components/Button, ../../icons/folder.svg, react, ./effects, react-router-dom, ../../utils/dataContext, ../../utils/appContext, ../../utils/translations
            📕 Functions: Files, Translated, Kks, Language, DocumentId, Title, handleClick, AddPadding
            📕 Stats: LOC 399 | funcs 8 | classes 0 | exports 0
        CreateFilteredExportData.ts
            📕 Imports: @tanstack/react-table, ../../utils/translations
            📕 Functions: createFilteredExportData
            📕 Exports: createFilteredExportData
            📕 Stats: LOC 48 | funcs 1 | classes 0 | exports 1
        effects.ts
            📕 Imports: axios, ../../utils/api
            📕 Exports: getTableData, getAppAttributes, getM3Children
            📕 Stats: LOC 72 | funcs 0 | classes 0 | exports 3
        📁 src/features/table/components/
            📄 Description:
            ColumnSearch.tsx
                📕 Imports: @tanstack/react-table, react, ../../../utils/translations
                📕 Functions: ColumnSearch, DebouncedInput
                📕 Exports: ColumnSearch
                📕 Stats: LOC 121 | funcs 2 | classes 0 | exports 1
            DownloadModal.tsx
                📕 Imports: react, ../../../utils/translations, ../../../icons/close_dark.svg, ../../../utils/dataContext, ../../../utils/api, ../effects, ../../../components/Button, jszip
                📕 Functions: DownloadModal, downloadAllFiles
                📕 Exports: DownloadModal
                📕 Stats: LOC 179 | funcs 2 | classes 0 | exports 1
            Pagination.tsx
                📕 Imports: ../../../icons/arrow_double_left.svg, ../../../icons/arrow_double_right.svg, ../../../icons/arrow_left.svg, ../../../icons/arrow_right.svg, ../../../utils/translations
                📕 Functions: Pagination
                📕 Exports: Pagination
                📕 Stats: LOC 79 | funcs 1 | classes 0 | exports 1
            Table.tsx
                📕 Imports: @tanstack/react-table, react, ../effects, ../../../components/Button, ../../../utils/translations, ../CreateColumns, ../../../icons/filter.svg, ../../../utils/appContext, ../../../utils/dataContext, react-csv, ../CreateFilteredExportData, ../../../icons/sort.svg, ../../../utils/useClickOutsideBounds, ./Pagination, ./ColumnSearch, ./DownloadModal
                📕 Functions: Table, sortTableData, createData, createRelatedDocId, createExportData
                📕 Exports: Table
                📕 Stats: LOC 453 | funcs 5 | classes 0 | exports 1
    📁 src/features/tour/
        📄 Description:
        steps.ts
            📕 Imports: ../../utils/translations
            📕 Functions: stepsMultiManual, stepsSingleManual, stepsTable
            📕 Exports: stepsMultiManual, stepsSingleManual, stepsTable
            📕 Stats: LOC 91 | funcs 3 | classes 0 | exports 3
        📁 src/features/tour/components/
            📄 Description:
            AppTour.tsx
                📕 Imports: @reactour/tour, react, react-router-dom, ../../../utils/dataContext, ../steps, ../../../icons/guide.svg, ../../../utils/translations
                📕 Functions: Tour
                📕 Exports: Tour
                📕 Stats: LOC 64 | funcs 1 | classes 0 | exports 1
📁 src/helpers/
    📄 Description:
    Search.ts
        📕 Functions: validateSearchInput
        📕 Exports: validateSearchInput
        📕 Stats: LOC 13 | funcs 1 | classes 0 | exports 1
📁 src/icons/
    📄 Description:
    📁 src/icons/languages/
        📄 Description:
        📁 src/icons/languages/old/
            📄 Description:
📁 src/images/
    📄 Description:
📁 src/pages/
    📄 Description:
    Dcc.tsx
        📕 Imports: react, react-router-dom, ../components/Page, ../features/breadcrumbs/useBreadcrumbs, ../features/table/components/Table, ../utils/appContext, ../utils/dataContext
        📕 Functions: DccTable
        📕 Exports: DccTable
        📕 Stats: LOC 27 | funcs 1 | classes 0 | exports 1
    Documents.tsx
        📕 Imports: react, ../components/Page, ../features/breadcrumbs/useBreadcrumbs, ../features/table/components/Table, ../utils/appContext, ../utils/dataContext
        📕 Functions: Documents
        📕 Exports: Documents
        📕 Stats: LOC 24 | funcs 1 | classes 0 | exports 1
    FAQ.tsx
        📕 Imports: react, ../components/Page, ../features/breadcrumbs/useBreadcrumbs, ../utils/translations, ../utils/dataContext
        📕 Functions: FAQ, Question
        📕 Exports: FAQ
        📕 Stats: LOC 44 | funcs 2 | classes 0 | exports 1
    Home.tsx
        📕 Imports: ../features/dashboard/components/Dashboard, react, ../features/breadcrumbs/useBreadcrumbs, ../utils/dataContext, ../features/dashboard/components/DashboardSearch, ../utils/appContext, ../components/Page, ../features/dashboard/components/ProjectTitle
        📕 Functions: Home
        📕 Exports: Home
        📕 Stats: LOC 28 | funcs 1 | classes 0 | exports 1
    Id.tsx
        📕 Imports: react, react-router-dom, ../components/Page, ../features/breadcrumbs/useBreadcrumbs, ../features/table/components/Table, ../utils/appContext, ../utils/dataContext
        📕 Functions: TablePage
        📕 Exports: TablePage
        📕 Stats: LOC 26 | funcs 1 | classes 0 | exports 1
    Kks.tsx
        📕 Imports: react, react-router-dom, ../components/Page, ../features/breadcrumbs/useBreadcrumbs, ../features/table/components/Table, ../utils/appContext, ../utils/dataContext
        📕 Functions: KksTable
        📕 Exports: KksTable
        📕 Stats: LOC 26 | funcs 1 | classes 0 | exports 1
    Search.tsx
        📕 Imports: react, react-router-dom, ../components/Page, ../features/breadcrumbs/useBreadcrumbs, ../features/search/components/SearchWindow, ../utils/appContext, ../utils/dataContext
        📕 Functions: Search
        📕 Exports: Search
        📕 Stats: LOC 24 | funcs 1 | classes 0 | exports 1
📁 src/utils/
    📄 Description:
    api.ts
        📕 Exports: BaseUrl, BaseUrl
        📕 Stats: LOC 2 | funcs 0 | classes 0 | exports 2
    appContext.ts
        📕 Imports: react
        📕 Exports: AppContext
        📕 Stats: LOC 35 | funcs 0 | classes 0 | exports 1
    dataContext.ts
        📕 Imports: react
        📕 Exports: DataContext
        📕 Stats: LOC 39 | funcs 0 | classes 0 | exports 1
    translations.ts
        📕 Imports: react, ./appContext
        📕 Functions: on
        📕 Exports: dictionary, T, useCurrentLanguage, useFallBackLanguage
        📕 Stats: LOC 2196 | funcs 1 | classes 0 | exports 4
    useClickOutsideBounds.ts
        📕 Imports: react
        📕 Functions: useClickOutsideBounds, checkIfClickedOutside
        📕 Exports: useClickOutsideBounds
        📕 Stats: LOC 22 | funcs 2 | classes 0 | exports 1
=== 📁 stylesheet/ ===
📄 Description:
coversheet.css
    📕 Stats: LOC 89 | funcs 0 | classes 0 | exports 0
    📕 Doc: selectors:14 media_queries:0
publish.sh
    📕 Imports: shebang:bash
    📕 Functions: merge_file
    📕 Stats: LOC 159 | funcs 1 | classes 0 | exports 0
    📕 Doc: Function to merge a single file
📁 stylesheet/coversheet/
    📄 Description:
    translations.xml
        📕 Stats: LOC 288 | funcs 0 | classes 0 | exports 0
        📕 Doc: root:strings tags:17
    📁 stylesheet/coversheet/img/
        📄 Description:
    📁 stylesheet/coversheet/xsl/
        📄 Description:
        BD001134.xsl
            📕 Functions: BD001134
            📕 Stats: LOC 82 | funcs 1 | classes 0 | exports 0
            📕 Doc: <xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xs="http://www.w3.org/2001/XMLSchema">
        BD001184.xsl
            📕 Functions: BD001184
            📕 Stats: LOC 80 | funcs 1 | classes 0 | exports 0
            📕 Doc: <xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xs="http://www.w3.org/2001/XMLSchema">
        BD001220U01.xsl
            📕 Functions: BD001220U01
            📕 Stats: LOC 95 | funcs 1 | classes 0 | exports 0
            📕 Doc: <xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xs="http://www.w3.org/2001/XMLSchema">
        BD001247U01.xsl
            📕 Functions: BD001247U01
            📕 Stats: LOC 82 | funcs 1 | classes 0 | exports 0
            📕 Doc: <xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xs="http://www.w3.org/2001/XMLSchema">
        default.xsl
            📕 Functions: default
            📕 Stats: LOC 77 | funcs 1 | classes 0 | exports 0
            📕 Doc: <xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xs="http://www.w3.org/2001/XMLSchema">
        html.xsl
            📕 Imports: default.xsl, BD001184.xsl, BD001220U01.xsl, BD001134.xsl
            📕 Functions: /
            📕 Stats: LOC 73 | funcs 1 | classes 0 | exports 0
            📕 Doc: <xsl:stylesheet version="2.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema">
📁 stylesheet/lib/
    📄 Description:
📁 stylesheet/prev_lib/
    📄 Description:
📁 stylesheet/toc/
    📄 Description:
    📁 stylesheet/toc/css/
        📄 Description:
        toc.css
            📕 Stats: LOC 239 | funcs 0 | classes 0 | exports 0
            📕 Doc: selectors:50 media_queries:1
    📁 stylesheet/toc/img/
        📄 Description:
    📁 stylesheet/toc/xsl/
        📄 Description:
        normalizeText.xsl
            📕 Stats: LOC 28 | funcs 0 | classes 0 | exports 0
            📕 Doc: <xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:xs="http://www.w3.org/2001/XMLSchema"
	xmlns:kit="publishing-toolkit"
	exclude-result-prefixes="xs"
	version="2.0">
        strings.xml
            📕 Stats: LOC 657 | funcs 0 | classes 0 | exports 0
            📕 Doc: root:strings tags:19
        toc.xsl
            📕 Imports: normalizeText.xsl
            📕 Functions: createContentsSection, createDisclaimer, test, /, *[@name = 'map' or contains(@class, '/map ')]
            📕 Stats: LOC 372 | funcs 5 | classes 0 | exports 0
            📕 Doc: <xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:xs="http://www.w3.org/2001/XMLSchema"
	xmlns:kit="publishing-toolkit"
	exclude-result-prefixes="#all"
	version="2.0">
📁 stylesheet/xsl/
    📄 Description:
    custAttMerger.xsl
        📕 Functions: /, *, map[processing-instruction('className') = 'S5_Manual'], processing-instruction()
        📕 Stats: LOC 121 | funcs 4 | classes 0 | exports 0
        📕 Doc: <xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:tps="http://www.kgu-group.com/tps"
    exclude-result-prefixes="xs" version="2.0">
    getAttributes.xsl
        📕 Functions: logAttribute, /, *, processing-instruction()
        📕 Stats: LOC 109 | funcs 4 | classes 0 | exports 0
        📕 Doc: <xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:xs="http://www.w3.org/2001/XMLSchema"
	xmlns:binder="https://www.uniqueue.se/SiemensAssemblyBinder.xsd"
	exclude-result-prefixes="#all"
	version="2.0">
    getAttributesList.xsl
        📕 Functions: attributes
        📕 Stats: LOC 49 | funcs 1 | classes 0 | exports 0
        📕 Doc: <xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:xs="http://www.w3.org/2001/XMLSchema"
	xmlns:binder="https://www.uniqueue.se/SiemensAssemblyBinder.xsd"
	exclude-result-prefixes="#all"
	version="2.0">
    levelGen.xsl
        📕 Functions: /, *, part|design|documentation, processing-instruction()
        📕 Stats: LOC 68 | funcs 4 | classes 0 | exports 0
        📕 Doc: <xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:xs="http://www.w3.org/2001/XMLSchema"
	xmlns:binder="https://www.uniqueue.se/SiemensAssemblyBinder.xsd"
	exclude-result-prefixes="#all"
	version="2.0">
    projectInformation.xsl
        📕 Functions: map[1]
        📕 Stats: LOC 18 | funcs 1 | classes 0 | exports 0
        📕 Doc: <xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    sorting.xsl
        📕 Functions: /
        📕 Stats: LOC 55 | funcs 1 | classes 0 | exports 0
        📕 Doc: <xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:xs="http://www.w3.org/2001/XMLSchema"
	xmlns:binder="https://www.uniqueue.se/SiemensAssemblyBinder.xsd"
	exclude-result-prefixes="#all"
	version="2.0">
    spaCompose.xsl
        📕 Functions: /, /*, *, topicmeta, documentation|design, mapref|partref|documentref|stopref|docref, processing-instruction()[not(../name()='documentation')][not(../name()='design')], processing-instruction('Doc_U0020_ID')[not(../name()='documentation')][not(../name()='design')], processing-instruction('kks')|processing-instruction('KKS'), title
        📕 Stats: LOC 133 | funcs 10 | classes 0 | exports 0
        📕 Doc: <xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:xs="http://www.w3.org/2001/XMLSchema"
	xmlns:binder="https://www.uniqueue.se/SiemensAssemblyBinder.xsd"
	exclude-result-prefixes="#all"
	version="2.0">