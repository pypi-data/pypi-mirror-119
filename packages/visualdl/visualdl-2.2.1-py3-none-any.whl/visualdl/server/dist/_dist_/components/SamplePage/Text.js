import e,{useCallback as _,useEffect as j,useState as C}from"../../../__snowpack__/pkg/react.js";import{borderRadius as i,ellipsis as y,em as T,rem as t,sameBorder as f,size as w,transitionProps as n}from"../../utils/style.js";import L,{useRunningRequest as N}from"../../hooks/useRequest.js";import R from"../Loader/ContentLoader.js";import q from"../Icon.js";import{TextChart as p}from"../Loader/ChartPage.js";import{getEntityUrl as I}from"./SampleChart.js";import z from"../../../__snowpack__/pkg/query-string.js";import u from"../../../__snowpack__/pkg/styled-components.js";import{useTranslation as F}from"../../../__snowpack__/pkg/react-i18next.js";const b=u.div`
    width: 100%;
`,E=u.h4`
    cursor: pointer;
    background-color: var(--text-chart-title-background-color);
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: ${t(40)};
    margin: 0;
    padding: 0 ${t(20)} 0 ${t(12)};
    border-radius: ${i};
    font-weight: 400;
    font-size: ${T(14)};
    ${n("background-color")}

    .tag {
        flex: auto;
        font-weight: 700;

        &::before {
            content: '';
            display: inline-block;
            ${w(t(10),t(3))}
            margin-right: ${t(8)};
            border-radius: ${t(1.5)};
            vertical-align: middle;
            background-color: var(--text-chart-title-indicator-color);
            ${n("background-color")}
        }
    }

    .run {
        flex: none;
        color: var(--text-lighter-color);
        ${n("color")}
        ${y()}
        max-width: 50%;

        &::before {
            content: '';
            display: inline-block;
            ${w(t(9),t(9))}
            margin-right: ${t(8)};
            border-radius: ${t(4.5)};
            vertical-align: middle;
            background-color: ${r=>r.color};
        }
    }

    .steps {
        flex: none;
        color: var(--text-lighter-color);
        margin-left: ${t(12)};
    }

    .icon {
        margin-left: ${t(20)};
        font-size: ${t(10)};
        color: var(--text-lighter-color);
        transform: rotate(${r=>r.opened?"180":"0"}deg);
        ${n(["transform","color"])};
    }
`,m=u.div`
    height: ${t(40)};
    margin-top: ${t(12)};
    display: flex;
    justify-content: flex-start;
    align-items: center;
    padding: 0;
    ${f(!0)}
    ${n("border-color")}
`,O=u.div`
    margin-top: ${t(12)};
    display: grid;
    grid-template-columns: fit-content(25%) auto;
    grid-row-gap: ${t(12)};
    justify-items: stretch;
    align-items: stretch;
    ${n("border-color")}

    > span {
        height: ${t(40)};
        line-height: 1.857142857;
        padding: ${t(7)} 0;
    }

    .step {
        ${f()}
        border-right: none;
        border-top-left-radius: ${i};
        border-bottom-left-radius: ${i};
        padding-left: ${t(8)};
        padding-right: ${t(14)};

        > span {
            display: block;
            width: 100%;
            color: var(--text-light-color);
            background-color: var(--text-chart-tag-background-color);
            padding: 0 ${t(8)};
            border-radius: ${i};
            ${n(["background-color","color"])}
        }
    }

    .text {
        ${f()}
        border-left: none;
        border-top-right-radius: ${i};
        border-bottom-right-radius: ${i};
        padding-right: ${t(20)};
        ${y()}

        > * {
            vertical-align: middle;
        }
    }
`,S=({run:r,tag:c,step:l,wallTime:h,index:s})=>{const{t:d}=F("sample"),{data:a,error:o,loading:g}=L(I("text",s,r,c,h),{dedupingInterval:5*60*1e3});return e.createElement(e.Fragment,null,e.createElement("span",{className:"step"},e.createElement("span",null,d("common:time-mode.step")," ",l)),e.createElement("span",{className:"text",title:a!=null?a:""},g?e.createElement(R,{viewBox:"0 0 640 16",height:"16"},e.createElement("rect",{x:"0",y:"0",rx:"3",ry:"3",width:(s+1)*250%640,height:"16"})):o!=null?o:a))},B=({run:r,tag:c,opened:l,running:h})=>{var x;const[s,d]=C(l!=null?l:!1);j(()=>d(l!=null?l:!1),[l]);const a=_(()=>d($=>!$),[]),{data:o,error:g,loading:v}=N(`/text/list?${z.stringify({run:r.label,tag:c})}`,!!h);return e.createElement(b,null,e.createElement(E,{color:r.colors[0],opened:s,onClick:a},e.createElement("span",{className:"tag"},c),e.createElement("span",{className:"run"},r.label),e.createElement("span",{className:"steps"},(x=o==null?void 0:o.length)!=null?x:0),e.createElement(q,{className:"icon",type:"chevron-down"})),s?v?e.createElement(e.Fragment,null,e.createElement(m,null,e.createElement(p,{width:270})),e.createElement(m,null,e.createElement(p,{width:640}))):g?e.createElement(m,null,g):e.createElement(O,null,o==null?void 0:o.map(($,k)=>e.createElement(S,{key:k,...$,run:r.label,tag:c,index:k}))):null)};export default B;export const Loader=()=>e.createElement(e.Fragment,null,e.createElement(b,null,e.createElement(E,{color:""}),e.createElement(m,null,e.createElement(p,{width:270})),e.createElement(m,null,e.createElement(p,{width:640}))),e.createElement(b,null,e.createElement(E,{color:""})));
