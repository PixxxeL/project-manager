import React from 'react';


export default class Loader extends React.Component {

    render() {
        return <div className="loader-tint">
            <div className="loader-wrapper">
                <i className="fa fa-spinner fa-spin fa-pulse fa-3x fa-fw"></i>
                <div className="text">Загружается...</div>
            </div>
        </div>;
    }

}
