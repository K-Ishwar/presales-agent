import axios from "axios";

const API = axios.create({
    baseURL: "http://localhost:8000"
});

export const uploadRFP = async (formData) => {

    return API.post(
        "/analyze",
        formData
    );

};

export const downloadPDF = async () => {

    return API.get(
        "/download-pdf",
        {
            responseType: "blob"
        }
    );

};

export const generateEmail = async () => {

    return API.get(
        "/email-draft"
    );

};