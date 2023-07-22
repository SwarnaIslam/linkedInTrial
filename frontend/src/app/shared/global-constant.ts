export class GlobalConstants {
    //message
    public static genericError:string = 'Something went wrong! Try again later.';

    // Regex
    public static nameRegex:string = '^[a-zA-Z ]*$';
    public static rollRegex:string = '^\d{4}$';
    public static emailRegex:string = '^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}\$';
    public static contactNumberRegex:string = '^\d{11}$';
    public static sessionRegex:string = '^\d{2}-\d{2}$';
    public static programLevelReges:string = '^[a-zA-Z]{2-4}$';

    // Variable 
    public static error:string = 'error';

}