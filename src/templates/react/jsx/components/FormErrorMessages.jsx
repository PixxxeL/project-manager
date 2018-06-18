import React from 'react';


const FormErrorMessages = props => {
    const errors = props.errors;
    return (
        errors && Array.isArray(errors) ?
        <div className="error-text">
            {errors.map(error => error.message).join(' ')}
        </div> :
        null
    );
}

export default FormErrorMessages;
