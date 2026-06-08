import axios from "axios";

const API = axios.create({
    baseURL: "http://localhost:8000"
});

export const uploadRFP = async (
    formData
) => {

    return API.post(
        "/upload-rfp",
        formData
    );

};

export const generateEmail = async (
    analysis,
    salesRepName
) => {

    return API.post(
        "/draft-email",
        {
            analysis,
            sales_rep_name:
                salesRepName
        }
    );

};

export const generateProposal = async (
    analysis,
    rfpText
) => {

    return API.post(
        "/generate-proposal",
        {
            analysis,
            rfp_text: rfpText
        },
        {
            responseType: "blob"
        }
    );

};