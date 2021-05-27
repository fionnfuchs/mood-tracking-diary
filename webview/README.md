# React Tailwind Boilerplate
React boilerplate with localization, router and Tailwind CSS configured 

## Included
- React + Router + Localization 
- Tailwind CSS 
- Basic Tailwind landing page components 

## Build & Run
### Build
```npm run build``` 

### Run
```npm start``` 

## Removing Landing Page components
If you want a fresh start with no landing page components: Remove all js files from /components except for App.js. Open App.js and remove components from render function and import statements. 

## Limitations
- Due to current create-react-app limitations PostCSS 8 plugins are not supported. Some work needs to be done to support things like PurgeCSS. 
- Localization is only minimally configured.