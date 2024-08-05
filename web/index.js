$(document).ready(function(){
    // Initially hide elements
    $('#main-menu').hide();
    $('#student-content').hide();
    $('#class-table-container').hide();

    // Role change handler (if needed for future enhancements)
    $('#role').change(function(){
        // Optional: Handle changes in the role selection
    });

    // Login button click event
    $('#login-btn').click(async function(){
        const selectedRole = $('#role').val();

        if (selectedRole === 'student') {
            const students = await eel.get_student_data()();
            
            // Populate the student dropdown
            const studentList = $('#student-list');
            studentList.empty(); // Clear previous options
            
            students.forEach(student => {
                if(student[0] && student[1] && student[3]) {
                    const option = $('<option></option>').val(student[0]).text(`${student[1]} (${student[3]})`);
                    $(option).data('student-info', student); // Store the entire student object
                    studentList.append(option);
                } else {
                    console.error('Student tuple is missing expected elements:', student);
                }
            });

            $('#student-content').show();
        } else {
            $('#student-content').hide();
        }

        await eel.send_data(selectedRole);
        //document.getElementById('myele').innerText = await eel.get_data()();
        $('#role-selection').hide();
        $('#main-menu').show();
    });

    // Load Classes button click event
    $('#load-classes-btn').click(async function(){
        const selectedOption = $('#student-list option:selected');
        const studentData = $(selectedOption).data('student-info'); // Retrieve the stored student data
    
        if (studentData) {
            // Send the student's data back to the Python backend to get the schedule
            const schedule = await eel.get_student_classes(studentData)(); // Pass the full student data
    
            // Populate the class table with the schedule data
            const classTableBody = $('#class-table tbody');
            classTableBody.empty(); // Clear previous rows
    
            schedule.forEach(cls => {
                if(cls[0] && cls[1] && cls[2] && cls[3] && cls[4] && cls[5]) {
                    const row = `<tr>
                                    <td>${cls[0]}</td>
                                    <td>${cls[1]}</td>
                                    <td>${cls[2]}</td>
                                    <td>${cls[3]}</td>
                                    <td>${cls[4]}</td>
                                    <td>${cls[5]}</td>
                                 </tr>`;
                    classTableBody.append(row);
                } else {
                    console.error('Class tuple is missing expected elements:', cls);
                }
            });
    
            $('#class-table-container').show();
        } else {
            $('#class-table-container').hide();
        }
    });
});